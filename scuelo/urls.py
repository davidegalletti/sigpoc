# urls.py

from django.urls import path
from .views import home_view , eleve_create_view

urlpatterns = [
    path('', home_view, name='home'),
    path("eleve-create/", eleve_create_view , name= "create")
    # Add other URL patterns for your CRUD operations and other views
]
