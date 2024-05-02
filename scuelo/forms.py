from django import forms
from .models import Eleve

class EleveCreationForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = "__all__" # Or specify the fields you want to include
