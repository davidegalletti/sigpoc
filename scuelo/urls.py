# urls.py

from django.urls import path
from .views  import ( StudentListView  , 
                     StudentPerClasseView , home   ,
                manage_payments, update_paiement, delete_payment ,
                manage_inscriptions ,  update_inscription , manage_annee_scolaire , update_annee_scolaire ,
                      StudentCreateView  , StudentUpdateView  ,  StudentDetailView , important_info
                     )


urlpatterns = [
    path('', home, name='home'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/create/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    #path('class/<int:class_id>/', StudentPerClasseView.as_view(), name='student_per_classe'),
    path('homepage/class/<int:class_id>/', StudentPerClasseView.as_view(), name='student_per_classe'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
     path('paiements/', manage_payments, name='manage_payments'),
    path('paiements/<int:pk>/update/', update_paiement, name='update_paiement'),
       # path('delete-paiement/<int:payment_id>/', delete_payment, name='delete_payment'),
         path('delete-paiement/<int:payment_id>/', delete_payment, name='delete_payment'), 
           path('inscriptions/', manage_inscriptions, name='manage_inscriptions'),# Note the name 'delete_payment'
  path('update-inscription/<int:pk>/', update_inscription, name='update_inscription'),
    path('update-annee-scolaire/<int:pk>/', update_annee_scolaire, name='update_annee_scolaire'),
 path('manage-annee-scolaire/', manage_annee_scolaire, name='manage_annee_scolaire'),
 path('important-info/', important_info, name='important_info'),
]# Add other URL patterns for your CRUD operations and other views
