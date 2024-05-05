# views.py

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Eleve , Classe ,Paiement
from .forms import EleveCreationForm
from django.views.generic import DetailView, ListView

from django.views.generic.edit import CreateView



def home_view(request):
    classes = Classe.objects.all()
    return render(request, 'scuelo/eleve_list.html' , {'classes' :classes}) 


# Create operation
def eleve_create_view(request):
    if request.method == 'POST':
        form = EleveCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eleve-list')  # Redirect to the list view
    else:
        form = EleveCreationForm()
    return render(request, 'scuelo/eleve_create.html', {'form': form})


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
        context['payments'] = Paiement.objects.filter(eleve_payment_id=student_id)
        return context

    def post(self, request, *args, **kwargs):
        student_id = self.kwargs['pk']
        montant = request.POST.get('montant')
        causal = request.POST.get('causal')
       # date_paiement = request.POST.get('date_paiement')
        #note_paiement = request.POST.get('note_paiement')
        
        
        #date_paiement =date_paiement, note_paiement=note_paiement
        # Add validation and error handling as needed
        Paiement.objects.create(montant=montant, causal=causal, eleve_payment_id=student_id)
        return redirect('student_detail', pk=student_id)
    
    

class CreatePaymentView(CreateView):
    model = Paiement
    fields = ['causal', 'montant' ,
              'date_paiement' ,'note_paiement'
              ]  # Specify the fields you want to include in the form
    template_name = 'scuelo/create_paiement.html'

    def form_valid(self, form):
        form.instance.eleve_payment_id = self.kwargs['pk']  # Set the student ID for the payment
        return super().form_valid(form)
    
    
    
class PaymentListView(ListView):
    model = Paiement
    template_name = 'scuelo/payment_list.html'
    context_object_name = 'payments'
    
    def get_queryset(self):
        student_id = self.kwargs.get('pk')
        return Paiement.objects.filter(eleve_payment_id=student_id)