# views.py
from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import  (render, redirect,
                               get_object_or_404 )
from .models import ( 
                     Eleve , Classe ,
                     Paiement  , Inscription
                    )
from .forms import ( StudentCreationForm , StudentUpdateForm , 
                    PaiementCreationForm , InscriptionForm 
                    
                )

from django.views.generic import (
    DetailView, ListView ,UpdateView 
                                  )

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy    , reverse


def home_view(request):
    classes = Classe.objects.all()
    return render(request, 'scuelo/scuelo_acceuil.html' , {'classes' :classes})

class CreateStudentView(CreateView):
    form_class = StudentCreationForm
    template_name = 'scuelo/eleve_create.html'
    success_url = '/homepage/acceuil/'
    
    # Optionally, you can override form_valid method to add additional 
    #logic after successful form submission
    
    def form_valid(self, form):
        # Add any additional logic here
        return super().form_valid(form)
    
    
def student_list(request , classe_id ):
    
    classes = Classe.objects.all()
    classe = get_object_or_404(Classe, pk=classe_id)
    students = classe.eleve_set.all()
    total_students = students.count()
    total_girls = students.filter(sex='F').count()
    total_boys = students.filter(sex='M').count()
    class_student_counts = []
    for classe in classes:
        total_students = classe.eleve_set.count()
        class_student_counts.append({'classe': classe, 'total_students': total_students})
    
    context = {
        'class_student_counts': class_student_counts,
        'classe': classe,
        'students': students,
        'total_students': total_students,
        'total_girls': total_girls,
        'total_boys': total_boys,
    }
    return render(request, 'scuelo/eleveperclasse.html', context)

class StudentDetailView(DetailView):
    model = Eleve
    template_name = 'scuelo/eleve_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['pk']
        payments = Paiement.objects.filter(eleve_payment_id=student_id)
        student = Eleve.objects.get(pk=student_id)
        total_payment = payments.aggregate(total=Sum('montant'))['total'] or 0  # Calculate total payment
        context['payments'] = payments
        context['total_payment'] = total_payment  # Add total payment to context
        
        context['inscriptions'] = student.inscriptions.all() 
        return context
    
    def post(self, request, *args, **kwargs):
        student_id = self.kwargs['pk']
        montant = request.POST.get('montant')
        causal = request.POST.get('causal')
  
        Paiement.objects.create(montant=montant, causal=causal, eleve_payment_id=student_id)
        return redirect('student_detail', pk=student_id)




def student_update(request, pk):
    student = Eleve.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=pk)  # Redirect to student detail page with updated student PK
    else:
        form = StudentUpdateForm(instance=student)
        # Check if reset button is clicked
        if 'reset' in request.GET:
            return redirect('student_detail', pk=pk)  # Redirect to student detail page without form submission
    return render(request, 'scuelo/eleve_update.html', {'form': form , 'student': student})




class CreatePaymentView(CreateView):
    model = Paiement
    form_class = PaiementCreationForm
    template_name = 'scuelo/create_paiement.html'
    
    def form_valid(self, form):
        form.instance.eleve_payment_id = self.kwargs['pk']  # Set the student ID for the payment
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eleve = get_object_or_404(Eleve, pk=self.kwargs['pk'])
        context['eleve'] = eleve
        return context
    
    
class PaymentListView(ListView):
    model = Paiement
    template_name = 'scuelo/payment_list.html'
    context_object_name = 'payments'
    
    def get_queryset(self):
        student_id = self.kwargs.get('pk')
        return Paiement.objects.filter(eleve_payment_id=student_id)

class PaymentUpdateView(UpdateView):
    model = Paiement
    fields = ['causal', 'montant', 'date_paiement', 'note_paiement']  # Specify the fields you want to update
    template_name = 'scuelo/paiement_update.html'  # Add your template name here
    success_url = reverse_lazy('homepage/student_detail')  # Specify the URL to redirect to after updatingeleve = get_object_or_404(Eleve, pk=eleve_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paiement = self.get_object()
        context['eleve'] = paiement.eleve_payment
        return context
 
 
 
 
from django.shortcuts import render, redirect
from .models import Inscription, Classe, AnneeScolaire, Eleve

def add_inscription(request, student_pk):
    student = Eleve.objects.get(pk=student_pk)  # Retrieve student for pre-population
    classes = Classe.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()
    context = {'student': student, 'classes': classes, 'annees_scolaires': annees_scolaires}

    if request.method == 'POST':
        classe_id = request.POST.get('classe')
        annee_scolaire_id = request.POST.get('annee_scolaire')

        classe = Classe.objects.get(pk=classe_id)
        annee_scolaire = AnneeScolaire.objects.get(pk=annee_scolaire_id)
        Inscription.objects.create(
            eleve=student, classe=classe, annee_scolaire=annee_scolaire
        )
        return redirect('success_url')  # Redirect to a success page after creation
    
    return render(request, 'add_inscription.html', context)



#### annee scolaire creation    views  
# 
#
# 
class CreateClasseView(CreateView):
    model = Classe
    fields = ['type_ecole', 'nom']
    template_name = 'scuelo/classe_create.html'
    success_url = '/acceuil/'

class UpdateClasseView(UpdateView):
    model = Classe
    fields = ['type_ecole', 'nom']
    template_name = 'scuelo/classe_update.html'
    success_url = '/acceuil/'

class CreateAnneeScolaireView(CreateView):
    model = AnneeScolaire
    fields = ['nom', 'date_initiale', 'date_finale', 'actuel']
    template_name = 'scuelo/annee_scolaire_create.html'
    success_url = '/acceuil/'

class UpdateAnneeScolaireView(UpdateView):
    model = AnneeScolaire
    fields = ['nom', 'date_initiale', 'date_finale', 'actuel']
    template_name = 'scuelo/annee_scolaire_update.html'
    success_url = '/acceuil/'