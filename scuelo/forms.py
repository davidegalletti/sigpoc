from django import forms
from .models import  (Eleve  , Paiement , 
                      Inscription ,Classe  ,  AnneeScolaire)

from .models  import CONDITION_ELEVE ,  CS_PY , HAND , SEX
from django.forms import inlineformset_factory



class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['classe', 'annee_scolaire']
        

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['causal', 'montant', 'date_paye', 'note', 'inscription']


class EleveCreateForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_enquete', 'condition_eleve', 'sex', 'date_naissance', 'cs_py', 'hand','parent', 'tel_parent', 'note_eleve', 'legacy_id']
        widgets = {
            'date_enquete': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'annee_inscr': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'condition_eleve': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'cs_py': forms.Select(attrs={'class': 'form-control'}),
            'hand': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_parent': forms.TextInput(attrs={'class': 'form-control'}),
            'note_eleve': forms.Textarea(attrs={'class': 'form-control'}),
            'legacy_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['classe', 'annee_scolaire']
        widgets = {
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'annee_scolaire': forms.Select(attrs={'class': 'form-control'}),
        }

InscriptionFormSet = forms.inlineformset_factory(
    Eleve, Inscription,
    form=InscriptionForm, extra=1, can_delete=True,
    min_num=1, validate_min=True
)
   
InscriptionFormSet = inlineformset_factory(Eleve, Inscription, fields=('classe', 'annee_scolaire'), extra=1, can_delete=True)

class EleveUpdateForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = [
            'nom', 'prenom', 'date_naissance', 'condition_eleve', 'sex', 
            'cs_py', 'date_enquete', 'hand', 'parent', 'tel_parent', 
            'note_eleve'
        ]  # Include fields for update
        widgets = {
            'cs_py': forms.Select(choices=CS_PY),
            'hand': forms.Select(choices=HAND),
            'condition_eleve': forms.Select(choices=CONDITION_ELEVE),
            'sex': forms.Select(choices=SEX),
            'note_eleve': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_enquete': forms.DateInput(attrs={'type': 'date'}),
            # Add widgets for other fields if necessary
        }

    def __init__(self, *args, **kwargs):
        super(EleveUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.instance and hasattr(self.instance, field_name):
                field.initial = getattr(self.instance, field_name)
                
                
InscriptionFormSet = inlineformset_factory(
    Eleve,
    Inscription,
    fields=('classe', 'annee_scolaire'),
    extra=1,  # Initial number of extra forms
    can_delete=True,
    widgets={
        'classe': forms.Select(),
        'annee_scolaire': forms.Select(),
    }
)
