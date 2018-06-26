from django.shortcuts import render
from .models import StudentInfo, StdSubject, Marks
from django.views.generic import TemplateView, ListView


class Homepage(ListView):
    template_name='results/home.html'
    model=StudentInfo


    
    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['obj']=StudentInfo.objects.all()
        return context
    
