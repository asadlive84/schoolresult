from django.shortcuts import render
from .models import StudentInfo, StdSubject, Marks
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Max,Avg,Sum
from .forms import ProfileSearchForm

class Homepage(ListView):
    template_name='results/home.html'
    model=StudentInfo
    form_class = ProfileSearchForm

    def get_queryset(self):
        try:
            name = self.kwargs['name']
        except:
            name = ''
        if (name != ''):
            object_list = self.StudentInfo.objects.filter(
                std_class__icontains=name)
        else:
            object_list = StudentInfo.objects.all()
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['obj']=StudentInfo.objects.all()
        
        return context
    


class StudentDetails(DetailView):
    template_name='results/student_details.html'
    model=StudentInfo

    

    def get_context_data(self, **kwargs):
        failed = 0
        std=self.kwargs['pk']
        context = super(StudentDetails, self).get_context_data(**kwargs)
        std_gpa=StudentInfo.objects.get(id=std)

        for i in std_gpa.marks_set.filter(subject_name__subject_type__startswith='R'):
            if i.subject_gpa=='F':
                failed = failed+1

        


        
        context['toatal_grade_point'] = ((std_gpa.marks_set.filter(
            subject_gradepoint__gte=1).aggregate(sp=Sum('subject_gradepoint')).get('sp', 0))/7)
        context['toatal_marks'] = ((std_gpa.marks_set.all().aggregate(
             sp=Sum('subject_marks')).get('sp', 0)))
        context['fail'] = failed
        return context
