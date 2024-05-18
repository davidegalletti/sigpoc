from django import forms
from .models import  (Eleve  , Paiement , 
                      Inscription ,Classe  ,  AnneeScolaire)

from django.forms import inlineformset_factory



class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['classe', 'annee_scolaire']
        
        
class EleveUpdateForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_naissance', 'condition_eleve', 'sex', 'cs_py', 'hand',  'parent', 'tel_parent', 'note_eleve']
        
InscriptionFormSet = inlineformset_factory(Eleve, Inscription, fields=('classe', 'annee_scolaire'), extra=1, can_delete=True)