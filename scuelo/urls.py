# urls.py

from django.urls import path
from .views  import ( StudentListView  , 
                     StudentPerClasseView , home   ,#  StudentDetailInPerClasseView ,
                manage_payments, update_paiement, delete_payment ,
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
     path('paiements/', manage_payments, name='manage_payments'),
    path('paiements/<int:pk>/update/', update_paiement, name='update_paiement'),
       # path('delete-paiement/<int:payment_id>/', delete_payment, name='delete_payment'),
         path('delete-paiement/<int:payment_id>/', delete_payment, name='delete_payment'),  # Note the name 'delete_payment'

    
]# Add other URL patterns for your CRUD operations and other views
