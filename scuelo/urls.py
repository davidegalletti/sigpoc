# urls.py

from django.urls import path
from .views import ( home_view ,# eleve_create_view ,
                    student_list ,StudentDetailView  ,
                    PaymentListView ,
                CreatePaymentView , student_update , 
                CreateStudentView ,
                PaymentUpdateView ,
                CreateClasseView,
                CreateAnneeScolaireView ,
                UpdateClasseView ,
                UpdateAnneeScolaireView
                ,add_inscription
                
                )

urlpatterns = [
    path('acceuil/', home_view, name='home'),
    
   # path("eleve-create/", eleve_create_view , name= "create"),
    path('acceuil/<int:classe_id>/students/', student_list, name='student_list'),
    path('create_student/', CreateStudentView.as_view(), name='create_student'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/payments/', PaymentListView.as_view(), name='payment_list'),
    path('student/<int:pk>/update/', student_update, name='student_update'),
    path('students/<int:pk>/create_payment/', CreatePaymentView.as_view(), name='create_payment'),
    path('payment/<int:pk>/update/', PaymentUpdateView.as_view(), name='update_payment'),
   # path('students/<int:pk>/inscription/', StudentInscriptionView.as_view(), name='student_inscription'),
#    
# 
  path('create_classe/', CreateClasseView.as_view(), name='create_classe'),
    path('update_classe/<int:pk>/', UpdateClasseView.as_view(), name='update_classe'),
    path('create_annee_scolaire/', CreateAnneeScolaireView.as_view(), name='create_annee_scolaire'),
    path('update_annee_scolaire/<int:pk>/', UpdateAnneeScolaireView.as_view(), name='update_annee_scolaire'),
    
     path('students/<int:pk>/add_inscription/', add_inscription, name='add_inscription'),
]# Add other URL patterns for your CRUD operations and other views
