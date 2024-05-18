from django import forms
from .models import  (Eleve  , Paiement , 
                      Inscription ,Classe  ,  AnneeScolaire)

from django.forms import inlineformset_factory



class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['classe', 'annee_scolaire']
        
class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = '__all__'

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = '__all__'

InscriptionFormSet = forms.inlineformset_factory(Eleve, Inscription, form=InscriptionForm, extra=1, can_delete=False)

class EleveUpdateForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_naissance', 'condition_eleve', 'sex', 'cs_py', 'hand',  'parent', 'tel_parent', 'note_eleve']
     

class EleveCreateForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_naissance', 'sex', 'condition_eleve', 'cs_py', 'hand', 'date_enquete', 'parent', 'tel_parent']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_enquete': forms.DateInput(attrs={'type': 'date'}),
        }
        
   
InscriptionFormSet = inlineformset_factory(Eleve, Inscription, fields=('classe', 'annee_scolaire'), extra=1, can_delete=True)
