# urls.py

from django.urls import path
from .views  import ( StudentListView  , 
                     StudentPerClasseView , home    , StudentDetailInPerClasseView ,
                     InscriptionUpdateView, 
                     EleveUpdateView , StudentCreateView 
                     )


urlpatterns = [
    path('', home, name='home'),
    path('students/', StudentListView.as_view(), name='student_list'),
    #path('students/create/', student_create, name='student_create'),
    
path('students/create/', StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/update/', EleveUpdateView.as_view(), name='student_update'),
    path('class/<int:class_id>/', StudentPerClasseView.as_view(), name='student_per_classe'),
    path('student/<int:pk>/class/<int:class_id>/', StudentDetailInPerClasseView.as_view(), name='student_detail_in_per_classe'),

    #path('student/<int:pk>/class/<int:class_id>/', StudentDetailInPerClasseView.as_view(), name='student_detail_in_per_classe'),
    path('inscription/<int:pk>/update/', InscriptionUpdateView.as_view(), name='inscription_update'),
     #path('student/<int:pk>/class/<int:class_id>/', StudentDetailInPerClasseView.as_view(), name='student_detaile'),
   
]# Add other URL patterns for your CRUD operations and other views
