# urls.py

from django.urls import path
from .views import ( home_view , eleve_create_view ,
                    student_list ,StudentDetailView  ,PaymentListView ,
                CreatePaymentView)

urlpatterns = [
    path('acceuil/', home_view, name='home'),
    
    path("eleve-create/", eleve_create_view , name= "create"),
    path('acceuil/<int:classe_id>/students/', student_list, name='student_list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/payments/', PaymentListView.as_view(), name='payment_list'),
     path('students/<int:pk>/create_payment/', CreatePaymentView.as_view(), name='create_payment'),
    # Add other URL patterns for your CRUD operations and other views
]
