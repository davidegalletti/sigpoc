
from django.shortcuts import render, get_object_or_404, redirect
from django_filters.views import FilterView
from django.urls import reverse_lazy ,  reverse
from django.views.generic.edit import UpdateView
from django.db import models
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.views.generic import DetailView , ListView 
from django.db.models import Count, Sum , Prefetch
from django.db.models import Q
from .forms import InscriptionForm , EleveUpdateForm, InscriptionFormSet , EleveCreateForm
from  .filters import EleveFilter
from .models import Eleve, Classe, Inscription, Paiement , AnneeScolaire
from django.forms import inlineformset_factory

def home(request):
    classes = Classe.objects.all()
    return render(request, 'scuelo/home.html', {'classes': classes})


class StudentListView(FilterView):
    model = Eleve
    template_name = 'scuelo/student/list.html'
    context_object_name = 'students'
    paginate_by = 10
    filterset_class = EleveFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) | Q(prenom__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        students = self.get_queryset()
        total_students = students.count()
        total_girls = students.filter(sex='F').count()
        total_boys = students.filter(sex='M').count()
        
        context['search_term'] = self.request.GET.get('q', '')
        total_fees = Paiement.objects.aggregate(total_fees=Sum('montant'))['total_fees'] or 0
        cs_py_sum = students.aggregate(cs_py_sum=Sum('cs_py'))['cs_py_sum'] or 0
        
        
        context.update({
            'total_students': total_students,
            'total_girls': total_girls,
            'total_boys': total_boys,
            'total_fees': total_fees,
            'cs_py_sum': cs_py_sum,
        })
        
        return context


    
class StudentPerClasseView(ListView):
    model = Eleve
    template_name = 'scuelo/student/perclasse.html'
    context_object_name = 'students'
    paginate_by = 12  # Number of students per page

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        query = self.request.GET.get('q')
        queryset = Eleve.objects.filter(inscription__classe__id=class_id).distinct()
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) | Q(prenom__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        class_id = self.kwargs.get('class_id')
        clicked_class = Classe.objects.get(pk=class_id)

        students = self.get_queryset()
        total_students = students.count()
        total_girls = students.filter(sex='F').count()
        total_boys = students.filter(sex='M').count()
        
        total_fees = Paiement.objects.filter(inscription__classe__id=class_id).aggregate(total_fees=Sum('montant'))[
                          'total_fees'] or 0
        cs_py_sum = students.aggregate(cs_py_sum=Sum('cs_py'))['cs_py_sum'] or 0

        context.update({
            'total_students': total_students,
            'total_girls': total_girls,
            'total_fees': total_fees,
            'total_boys' : total_boys,
            'cs_py_sum': cs_py_sum,
            'clicked_class': clicked_class,
        })

        return context
    
#view detail  in per classe 
# 

class StudentDetailInPerClasseView(DetailView):
    model = Eleve
    template_name = 'scuelo/student/detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        return Eleve.objects.filter(inscription__classe__id=class_id).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        class_id = self.kwargs.get('class_id')
        clicked_class = Classe.objects.get(pk=class_id)

        student = self.object
        inscriptions = student.inscription_set.all()
        payments = Paiement.objects.filter(inscription__in=inscriptions)

        total_students = Eleve.objects.filter(inscription__classe__id=class_id).count()
        total_girls = Eleve.objects.filter(inscription__classe__id=class_id, sex='F').count()
        total_boys = Eleve.objects.filter(inscription__classe__id=class_id, sex='M').count()
        
        total_fees = payments.aggregate(total_fees=Sum('montant'))['total_fees'] or 0
        cs_py_sum = Eleve.objects.filter(inscription__classe__id=class_id).aggregate(cs_py_sum=Sum('cs_py'))['cs_py_sum'] or 0

        # Additional information
        parents = f"{student.parent} ({student.tel_parent})"
        notes = student.note_eleve

        context.update({
            'inscriptions': inscriptions,
            'payments': payments,
            'total_students': total_students,
            'total_girls': total_girls,
            'total_boys': total_boys,
            'total_fees': total_fees,
            'cs_py_sum': cs_py_sum,
            'clicked_class': clicked_class,
            'parents': parents,
            'notes': notes,
        })

        # Initialize the form
        form = InscriptionForm()

        if self.request.method == 'POST':
            form = InscriptionForm(self.request.POST)
            if form.is_valid():
                new_inscription = form.save(commit=False)
                new_inscription.eleve = student
                new_inscription.save()
                return redirect('student_detail_in_per_classe', pk=student.id, class_id=class_id)
        
        # Pass the form to the context
        context['form'] = form
        
        return context

#  inscription 
# 
class InscriptionUpdateView(UpdateView):
    model = Inscription
    form_class = InscriptionForm
    template_name = 'scuelo/inscriptions/update.html'

    def get_success_url(self):
        student = self.object.eleve
        class_id = self.kwargs.get('class_id')
        return reverse_lazy('student_detail_in_per_classe', kwargs={'pk': student.pk, 'class_id': class_id})
    
class EleveUpdateView(UpdateView):
    model = Eleve
    form_class = EleveUpdateForm
    template_name = 'scuelo/student/update.html'

    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.object.pk, 'class_id': self.object.classe.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['inscription_formset'] = InscriptionFormSet(self.request.POST, instance=self.object)
        else:
            context['inscription_formset'] = InscriptionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        inscription_formset = context['inscription_formset']
        if inscription_formset.is_valid():
            self.object = form.save()
            inscription_formset.instance = self.object
            inscription_formset.save()
            
            # Update student's class based on the latest inscription
            latest_inscription = self.object.inscription_set.latest('id')
            self.object.classe = latest_inscription.classe
            self.object.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
class StudentCreateView(CreateView):
    model = Eleve
    form_class = EleveCreateForm
    template_name = 'scuelo/student/create.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['inscription_formset'] = InscriptionFormSet(self.request.POST)
        else:
            data['inscription_formset'] = InscriptionFormSet()
        data['classes'] = Classe.objects.all()
        data['annees_scolaires'] = AnneeScolaire.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        inscription_formset = context['inscription_formset']
        if inscription_formset.is_valid():
            self.object = form.save()
            inscription_formset.instance = self.object
            inscription_formset.save()
            return redirect('student_detail_in_per_classe', pk=self.object.pk)  # Corrected redirection
        else:
            return self.render_to_response(self.get_context_data(form=form))