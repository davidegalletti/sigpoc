from django import forms
from .models import Eleve  , Paiement

class StudentCreationForm(forms.ModelForm):
     class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_enquete', 'condition_eleve', 'sex', 'date_naissance',
                  'cs_py', 'hand', 'annee_inscr', 'parent', 
                  'tel_parent', 'note_eleve', 'classe_nass'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_enquete': forms.DateInput(attrs={'class': 'form-control'}),
            'condition_eleve': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control'}),
            'cs_py': forms.Select(attrs={'class': 'form-control'}),
            'hand': forms.Select(attrs={'class': 'form-control'}),
            'annee_inscr': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_parent': forms.TextInput(attrs={'class': 'form-control'}),
            'note_eleve': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'classe_nass': forms.Select(attrs={'class': 'form-control'}),
        }


            


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_enquete', 'condition_eleve', 'sex', 'date_naissance',
                  'cs_py', 'hand', 'annee_inscr', 'parent',
                  'tel_parent', 'note_eleve', 'classe_nass'
                  ]
        
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_enquete': forms.DateInput(attrs={'class': 'form-control'}),
            'condition_eleve': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control'}),
            'cs_py': forms.Select(attrs={'class': 'form-control'}),
            'hand': forms.Select(attrs={'class': 'form-control'}),
            'annee_inscr': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_parent': forms.TextInput(attrs={'class': 'form-control'}),
            'note_eleve': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'classe_nass': forms.Select(attrs={'class': 'form-control'}),
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






class   InscriptionForm(forms.CaseForm):
    
    pass

