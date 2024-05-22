# urls.py

from django.urls import path
from .views  import ( StudentListView  , 
                     StudentPerClasseView , home   ,#  StudentDetailInPerClasseView ,
                     InscriptionUpdateView,  PaiementCreateView, 
                      StudentCreateView  , StudentUpdateView  ,  StudentDetailView
                     )


urlpatterns = [
    path('', home, name='home'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/create/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    #path('class/<int:class_id>/', StudentPerClasseView.as_view(), name='student_per_classe'),
    path('homepage/class/<int:class_id>/', StudentPerClasseView.as_view(), name='student_per_classe'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    #path('homepage/student/<int:pk>/class/<int:class_id>/', StudentDetailInPerClasseView.as_view(), name='student_detail_in_per_classe'),
    #path('student/<int:pk>/class/<int:class_id>/', StudentDetailInPerClasseView.as_view(), name='student_detail_in_per_classe'),
    path('create/paiement/', PaiementCreateView.as_view(), name='create_paiement'),

    path('inscription/<int:pk>/update/', InscriptionUpdateView.as_view(), name='inscription_update'),
   
]# Add other URL patterns for your CRUD operations and other views
