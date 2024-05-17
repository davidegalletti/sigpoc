from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Count, Sum
from .models import Eleve, Classe, Inscription, Paiement

class StudentListView(ListView):
    model = Eleve
    template_name = 'scuelo/student/list.html'
    context_object_name = 'students'

    #def get_queryset(self):
        #return Eleve.objects.all().select_related('inscription__classe')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        students = self.get_queryset()
        total_students = students.count()
        total_girls = students.filter(sex='F').count()
        total_fees = Paiement.objects.aggregate(total_fees=Sum('montant'))['total_fees'] or 0
        cs_py_sum = students.aggregate(cs_py_sum=Sum('cs_py'))['cs_py_sum'] or 0
        
        context.update({
            'total_students': total_students,
            'total_girls': total_girls,
            'total_fees': total_fees,
            'cs_py_sum': cs_py_sum,
        })
        
        return context
