from django.shortcuts import render
from django.http import HttpResponse
from .models  import ( Classe , Eleve )
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Count, Sum, F
from .models import Classe, Eleve, Inscription, Paiement

def index(request):
    from django.core import management
    management.call_command('fixtures')
    return HttpResponse("Hello, world.")


