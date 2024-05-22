
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from django.views.generic import FormView
from django.urls import reverse_lazy ,  reverse
from django.views.generic.edit import UpdateView
from django.db import  transaction
from django.views.generic import CreateView
from django.views.generic import ( DetailView , ListView  ,TemplateView,  
                                ListView, CreateView, UpdateView, DeleteView 
)
from django.db.models import Q  , Max , F , Sum
from .forms import  ( InscriptionForm , InscriptionFormSet 
    , EleveCreateForm ,  EleveUpdateForm , PaiementForm 
)
from  .filters import EleveFilter
from .models import Eleve, Classe, Inscription, Paiement , AnneeScolaire
from django.forms import inlineformset_factory


def home(request):
    classes = Classe.objects.all()
    return render(request, 'scuelo/home.html', {'classes': classes})

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
            with transaction.atomic():
                self.object = form.save()
                inscription_formset.instance = self.object
                inscription_formset.save()
            return redirect('home')  # Use reverse for redirection reverse('student_detail', kwargs={'pk': self.object.pk})
        else:
            return self.render_to_response(self.get_context_data(form=form))


    
class StudentPerClasseView(ListView):
    model = Eleve
    template_name = 'scuelo/student/perclasse.html'
    context_object_name = 'students'
    #paginate_by = 12  # Number of students per page

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')

        # Get the latest inscription for each student in the specified class
        latest_inscriptions = Inscription.objects.filter(classe_id=class_id).values('eleve_id').annotate(last_inscription=Max('date_inscription'))

        # Get the IDs of the students with the latest inscription in the specified class
        student_ids = [inscription['eleve_id'] for inscription in latest_inscriptions]

        # Exclude students who have an earlier inscription for the same class
        queryset = Eleve.objects.filter(id__in=student_ids)

        query = self.request.GET.get('q')
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
        
        total_fees = Paiement.objects.filter(inscription__classe__id=class_id).aggregate(total_fees=Sum('montant'))['total_fees'] or 0
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
    

class StudentDetailView(DetailView):
    model = Eleve
    template_name = 'scuelo/student/detail.html'
    context_object_name = 'student'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object

        # Fetch inscriptions related to the student
        inscriptions = Inscription.objects.filter(eleve=student)

        # Fetch payments related to the student (via inscriptions)
        payments = Paiement.objects.filter(inscription__in=inscriptions)

        context['inscriptions'] = inscriptions
        context['payments'] = payments
        return context

'''
class StudentDetailInPerClasseView(DetailView):
    model = Eleve
    template_name = 'scuelo/student/detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        student_id = self.kwargs.get('pk')
        return Eleve.objects.filter(inscription__classe__id=class_id, pk=student_id).distinct()


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
        
        return context'''

    

class StudentListView(FilterView):
    model = Eleve
    template_name = 'scuelo/student/list.html'
    context_object_name = 'students'
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


    

class StudentUpdateView(UpdateView):
    model = Eleve
    form_class = EleveUpdateForm
    template_name = 'scuelo/student/update.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['inscription_formset'] = InscriptionFormSet(self.request.POST, instance=self.object)
        else:
            data['inscription_formset'] = InscriptionFormSet(instance=self.object)
        data['classes'] = Classe.objects.all()
        data['annees_scolaires'] = AnneeScolaire.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        inscription_formset = context['inscription_formset']
        if inscription_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                # Remove the student from the previous class if the class has changed
                inscription_formset.instance = self.object
                inscription_formset.save()
            return redirect(reverse('student_detail', kwargs={'pk': self.object.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=form))  


    
