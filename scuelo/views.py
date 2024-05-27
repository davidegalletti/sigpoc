
from django.shortcuts import render, redirect , get_object_or_404
from django_filters.views import FilterView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.forms import modelformset_factory
from django.urls import reverse_lazy ,  reverse
from django.views.generic.edit import UpdateView
from django.db import  transaction , models
from django.views.generic import CreateView
from django.views.generic import ( DetailView , ListView  , View,  
                                ListView, CreateView, UpdateView, DeleteView  , 
)
from django.db.models import Q  , Max , F , Sum , Count
from .forms import  ( InscriptionForm , InscriptionFormSet 
    , EleveCreateForm ,  EleveUpdateForm , PaiementForm  , AnneeScolaireForm ,  PaiementPerStudentForm
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
         # Annotate queryset with total payment for each student
        queryset = queryset.annotate(total_payment=Sum('inscription__paiement__montant'))


        
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
        total_cs = students.filter(cs_py='C').count()
        total_extra = students.filter(cs_py='E').count()
        total_py = students.filter(cs_py='P').count()
        total_acc = students.filter(cs_py='A').count()
        total_bravo = students.filter(cs_py='B').count()
        total_good_condition = students.filter(condition_eleve='CONF').count()
        total_abandon = students.filter(condition_eleve='ABAN').count()
        total_prop = students.filter(condition_eleve='PROP').count()
        total_fees = Paiement.objects.filter(inscription__classe__id=class_id).aggregate(total_fees=Sum('montant'))['total_fees'] or 0
        #cs_py_sum = students.aggregate(cs_py_sum=Sum('cs_py'))['cs_py_sum'] or 0

        context.update({
            'total_students': total_students,
            'total_girls': total_girls,
            'total_fees': total_fees,
            'total_boys' : total_boys,
            'total_cs': total_cs,
            'total_extra': total_extra,
            'total_py': total_py,
            'total_acc': total_acc,
            'total_bravo': total_bravo,
            'clicked_class': clicked_class,
            'total_good_condition': total_good_condition,
            'total_abandon': total_abandon,
            'total_prop': total_prop,
            
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

        # Calculate the total payment for the student
        total_payment = payments.aggregate(total=Sum('montant'))['total'] or 0

        context['inscriptions'] = inscriptions
        context['payments'] = payments
        context['total_payment'] = total_payment
        
        context['form'] = PaiementPerStudentForm()  # Add the payment form to the context
        return context

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
        
def calculate_tenue(classe, montant):
    # Define the rules for counting tenues based on class and montant
    if classe in ['PS', 'GS', 'MS']:
        if montant == 4000:
            return 2
        elif montant == 2000:
            return 1
    else:
        if montant == 4500:
            return 2
        elif montant == 2250:
            return 1
    # Return 0 if no matching rule is found
    return 0

def manage_payments(request):
    causal_filter = request.GET.get('causal')
    search_query = request.GET.get('search')

    # Retrieve all payments
    payments = Paiement.objects.all()

    # Filter payments with causal 'tenue'
    tenue_payments = Paiement.objects.filter(causal='TEN')

    if search_query:
        # Filter payments based on the student's name (nom or prenom)
        payments = payments.filter(inscription__eleve__nom__icontains=search_query) | \
                   payments.filter(inscription__eleve__prenom__icontains=search_query)

    if causal_filter:
        payments = payments.filter(causal=causal_filter)

    # Pagination code (if needed)

    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paiement ajouté avec succès.')
            return redirect('manage_payments')
    else:
        form = PaiementForm()

    # Calculate total montant per causal category
    total_montant_per_causal = payments.values('causal').annotate(total_montant=Sum('montant'))

    # Calculate total fees for each causal category
    total_tenues = 0
    payment_details = []
    for payment in tenue_payments:
        classe = payment.inscription.classe.type_ecole
        montant = payment.montant
        total_tenues += calculate_tenue(classe, montant)
        # Fetch nom_classe
        nom_classe = payment.inscription.classe.nom
        payment_details.append({'payment': payment, 'nom_classe': nom_classe})

  
    total_payments_count = payments.count()
    total_montant_all_payments = payments.aggregate(total_montant_all_payments=Sum('montant'))['total_montant_all_payments']
        

    return render(request, 'scuelo/paiment/manage.html', {
        'form': form,
        'payments': payments,
        'causal_filter': causal_filter,
        'search_query': search_query,
        'total_tenues': total_tenues,
        'payment_details': payment_details,
        'total_montant_per_causal': total_montant_per_causal,
        'total_payments_count': total_payments_count,  # Pass the count to the template
        'total_montant_all_payments': total_montant_all_payments
    })


@method_decorator(csrf_exempt, name='dispatch')
class AddPaiementAjaxView(View):
    def post(self, request, *args, **kwargs):
        student_id = kwargs['pk']
        student = get_object_or_404(Eleve, pk=student_id)
        form = PaiementPerStudentForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.inscription = Inscription.objects.filter(eleve=student).last()
            paiement.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
def update_paiement(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    eleve = paiement.inscription.eleve
    classe = paiement.inscription.classe
    

    if request.method == 'POST':
        form = PaiementForm(request.POST, instance=paiement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paiement mis à jour avec succès.')
            return redirect('manage_payments')
    else:
        form = PaiementForm(instance=paiement, initial={'creation_date': paiement.date_paye})  

    return render(request, 'scuelo/paiment/update.html', {
        'form': form,
        'paiement': paiement,
        'eleve': eleve,
        'classe': classe
    })


def delete_payment(request, payment_id):
    if request.method == 'POST':
        payment = get_object_or_404(Paiement, pk=payment_id)
        payment.delete()
        messages.success(request, 'Payment deleted successfully.')
        return redirect('manage_payments')
    else:
        return redirect('manage_payments') 
    

def manage_inscriptions(request):
    # Handle form submission
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_inscriptions') 
    else:
        form = InscriptionForm()
        
    # Fetch all classes
    classes = Classe.objects.all()

    # Get class name filter from query parameters
    class_name_filter = request.GET.get('class')

    # Get search query from query parameters
    search_query = request.GET.get('search')

    # Get all inscriptions
    inscriptions = Inscription.objects.all()

    # Filter inscriptions by school year
    year_filter = request.GET.get('annee_scolaire')
    if year_filter:
        inscriptions = inscriptions.filter(annee_scolaire__nom=year_filter)

    # Filter inscriptions by class name
    if class_name_filter:
        inscriptions = inscriptions.filter(classe__nom=class_name_filter)

    # Filter inscriptions by search query
    if search_query:
        inscriptions = inscriptions.filter(Q(eleve__nom__icontains=search_query) | Q(eleve__prenom__icontains=search_query))

    # Calculate total number of inscriptions
    total_inscriptions = inscriptions.count()

    # Calculate inscriptions per class
    inscriptions_per_class = inscriptions.values('classe__nom').annotate(total=Count('id')).order_by('classe__nom')

    # Calculate inscriptions per school year
    inscriptions_per_year = Inscription.objects.values('annee_scolaire__nom').annotate(total=Count('id')).order_by('annee_scolaire__nom')

    # Paginate the inscriptions
    paginator = Paginator(inscriptions, 10)  # Show 10 inscriptions per page
    page = request.GET.get('page')
    inscriptions = paginator.get_page(page)

    return render(request, 'scuelo/inscriptions/manage.html', {
        'form': form,
        'classes': classes,
        'class_name_filter': class_name_filter,
        'inscriptions': inscriptions,
        'total_inscriptions': total_inscriptions,
        'inscriptions_per_class': inscriptions_per_class,
        'inscriptions_per_year': inscriptions_per_year,
        'year_filter': year_filter,
        'search_query': search_query,
    })


def update_inscription(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)
    if request.method == 'POST':
        form = InscriptionForm(request.POST, instance=inscription)
        if form.is_valid():
            form.save()
            return redirect('manage_inscriptions')
    else:
        form = InscriptionForm(instance=inscription)

    return render(request, 'scuelo/inscriptions/update.html', {
        'form': form,
        'inscription': inscription
    })
    
    
def manage_annee_scolaire(request):
    # Fetch all existing Annee Scolaire objects
    annee_scolaires = AnneeScolaire.objects.all()

    annee_scolaires = AnneeScolaire.objects.annotate(
        total_students=Count('inscription__eleve', distinct=True),
        total_girls=Count('inscription__eleve', filter=Q(inscription__eleve__sex='F'), distinct=True),
        total_boys=Count('inscription__eleve', filter=Q(inscription__eleve__sex='M'), distinct=True)
    )

    if request.method == 'POST':
        form = AnneeScolaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_annee_scolaire')  # Redirect to the same page after form submission
    else:
        form = AnneeScolaireForm()  # Create a new form instance

    return render(request, 'scuelo/anne_scolaire/manage.html', {
        'annee_scolaires': annee_scolaires,
        'form': form,
    })
    
    
def update_annee_scolaire(request, pk):
    annee_scolaire = get_object_or_404(AnneeScolaire, pk=pk)
    if request.method == 'POST':
        form = AnneeScolaireForm(request.POST, instance=annee_scolaire)
        if form.is_valid():
            form.save()
            return redirect('manage_annee_scolaire')  # Redirect to the manage view after update
    else:
        form = AnneeScolaireForm(instance=annee_scolaire)
    return render(request, 'scuelo/anne_scolaire/update.html', {'form': form , 'annee_scolaire': annee_scolaire })



def important_info(request):
    tenue_payments = Paiement.objects.filter(causal='TEN')

    # Calculate total fees for 'tenue'
    total_tenues = 0
    for payment in tenue_payments:
        classe = payment.inscription.classe.type_ecole
        montant = payment.montant
        total_tenues += calculate_tenue(classe, montant)

    # Calculate total montant per causal category
    total_montant_per_causal = Paiement.objects.values('causal').annotate(total_montant=Sum('montant'))

    # Count total number of payments
    total_payments_count = Paiement.objects.count()

    # Calculate total montant of all payments
    total_montant_all_payments = Paiement.objects.aggregate(total_montant_all_payments=Sum('montant'))['total_montant_all_payments']

    return render(request, 'scuelo/dashboard.html', {
        'total_tenues': total_tenues,
        'total_montant_per_causal': total_montant_per_causal,
        'total_payments_count': total_payments_count,
        'total_montant_all_payments': total_montant_all_payments
    })