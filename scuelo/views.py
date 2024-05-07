# views.py
from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Eleve , Classe ,Paiement
from .forms import StudentCreationForm , StudentUpdateForm
from django.views.generic import DetailView, ListView
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy 


def home_view(request):
    classes = Classe.objects.all()
    return render(request, 'scuelo/scuelo_acceuil.html' , {'classes' :classes})




class CreateStudentView(CreateView):
    form_class = StudentCreationForm
    template_name = 'scuelo/eleve_create.html'
    success_url = '/homepage/acceuil/'
    
    # Optionally, you can override form_valid method to add additional logic after successful form submission
    def form_valid(self, form):
        # Add any additional logic here
        return super().form_valid(form)

def student_list(request, classe_id):
    classe = get_object_or_404(Classe, pk=classe_id)
    students = classe.eleve_set.all()
    return render(request, 'scuelo/eleveperclasse.html', {'classe': classe, 'students': students})



class StudentDetailView(DetailView):
    model = Eleve
    template_name = 'scuelo/eleve_detail.html'
    context_object_name = 'student'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['pk']
        payments = Paiement.objects.filter(eleve_payment_id=student_id)
        total_payment = payments.aggregate(total=Sum('montant'))['total'] or 0  # Calculate total payment
        context['payments'] = payments
        context['total_payment'] = total_payment  # Add total payment to context
        return context
    
    def post(self, request, *args, **kwargs):
        student_id = self.kwargs['pk']
        montant = request.POST.get('montant')
        causal = request.POST.get('causal')
        #date_paiement = request.POST.get('date_paiement')
        #note_paiement = request.POST.get('note_paiement')
        
        
        #date_paiement =date_paiement, note_paiement=note_paiement
        # Add validation and error handling as needed
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
    
    return render(request, 'scuelo/eleve_update.html', {'form': form})
'''
def student_update(request, pk):
    student = Eleve.objects.get(pk=pk)
    #good = reverse_lazy(student, "pk")
    #success_url = '/homepage/acceuil/'
    
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail' ,   pk=pk)
    else: # pk=student
        form = StudentUpdateForm(instance=student)
    
    
    return render(request, 'scuelo/eleve_update.html', {'form': form})'''


class CreatePaymentView(CreateView):
    model = Paiement
    fields = ['causal', 'montant' ,
              'date_paiement' ,'note_paiement'
              ]  # Specify the fields you want to include in the form
    template_name = 'scuelo/create_paiement.html'
    
    
    
    def form_valid(self, form):
        form.instance.eleve_payment_id = self.kwargs['pk']  # Set the student ID for the payment
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.kwargs['pk']})
    
    
    
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
    success_url = reverse_lazy('homepage/student_detail')  # Specify the URL to redirect to after updating