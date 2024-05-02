# views.py

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Eleve
from .forms import EleveCreationForm


def home_view(request):
    return render(request, 'base.html')


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