from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    from django.core import management
    management.call_command('fixtures')
    return HttpResponse("Hello, world.")
