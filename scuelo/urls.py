# urls.py

from django.urls import path
from .views  import  StudentListView       

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student_list'),
    
   
]# Add other URL patterns for your CRUD operations and other views
