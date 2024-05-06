from django import forms
from .models import Eleve

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_enquete', 
                  'condition_eleve', 'sex',
                  'date_naissance', 'cs_py', 'hand',
                  'annee_inscr', 'parent', 'tel_parent', 
                  'note_eleve', 'classe_nass'
                  ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling or attributes if needed
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})  
            


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'date_enquete', 'condition_eleve', 'sex', 'date_naissance',
                  'cs_py', 'hand', 'annee_inscr', 'parent', 
                  'tel_parent', 'note_eleve', 'classe_nass']