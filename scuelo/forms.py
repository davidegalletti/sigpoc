from django import forms
from .models import  (Eleve  , Paiement , 
                      Inscription ,Classe  ,  AnneeScolaire)


class StudentCreationForm(forms.ModelForm):
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    annee_scolaire = forms.ModelChoiceField(queryset=AnneeScolaire.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_enquete', 'condition_eleve', 'sex', 'date_naissance', 'cs_py', 'hand', 'parent', 'tel_parent', 'note_eleve']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_enquete': forms.DateInput(attrs={'class': 'form-control'}),
            'condition_eleve': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control'}),
            'cs_py': forms.Select(attrs={'class': 'form-control'}),
            'hand': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_parent': forms.TextInput(attrs={'class': 'form-control'}),
            'note_eleve': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }




class StudentUpdateForm(forms.ModelForm):
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    annee_scolaire = forms.ModelChoiceField(queryset=AnneeScolaire.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_enquete', 'condition_eleve', 'sex', 'date_naissance', 'cs_py', 'hand', 'parent', 'tel_parent', 'note_eleve']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_enquete': forms.DateInput(attrs={'class': 'form-control'}),
            'condition_eleve': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control'}),
            'cs_py': forms.Select(attrs={'class': 'form-control'}),
            'hand': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_parent': forms.TextInput(attrs={'class': 'form-control'}),
            'note_eleve': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }




class PaiementCreationForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['causal', 'montant', 'date_paiement', 'note_paiement']
        widgets = {
            'causal': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_paiement': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'note_paiement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }





class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['classe', 'annee_scolaire']