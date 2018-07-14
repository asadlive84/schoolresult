from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # new
from .models import StudentInfo, StdSubject, Marks,Rank
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,FormView
from django.db.models import Max,Avg,Sum
from django.views.generic.edit import FormMixin
from .forms import ProfileSearchForm, AddStudentInfo, StudentUpdateForm, StudentSubjectGPAForm, StudentSubjectGPAFormAdd, Addmarks, ResultSearchForm, SubjectSearchForm, ClassSearchForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


from django.db.models import Avg, Max, Min

from django.utils import timezone

from .render import *



class Homepage(TemplateView,FormMixin):
    template_name='results/home.html'
   
    form_class = ResultSearchForm

    
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
    
        form = self.form_class(request.POST)
        if form.is_valid():
           try:
               self.object_search = StudentInfo.objects.get(std_roll=form.cleaned_data['std_roll_form'], std_class=form.cleaned_data['std_class_form'])
           except:
               self.object_search=False
               print(self.object_search)
           
        context['std_search']=self.object_search

        try:
            context['ranks'] = Rank.objects.get(std=self.object_search)
        except:
            context['ranks']='Fail'




        #context['ranks'] = Rank.objects.get(std=self.object_search)
        #self.object_search.marks
           

        return super(Homepage, self).render_to_response(context)


    

        
   
    
    
    

class StudentDetails(DetailView):
    template_name = 'results/student_details.html'
    model=StudentInfo
    #login_url = 'login'  # new

    

    def get_context_data(self, **kwargs):
        failed = 0
        same_subject=[]
        std=self.kwargs['pk']
        context = super(StudentDetails, self).get_context_data(**kwargs)
        std_gpa=StudentInfo.objects.get(id=std)

        for i in std_gpa.marks_set.filter(subject_name__subject_type__startswith='R').order_by('-pub_date'):

            if i.subject_name not in same_subject:
                same_subject.append(i.subject_name)
                if i.subject_gpa == 'F':
                    failed = failed+1

        
        context['subject_max_number'] = std_gpa.marks_set.all().aggregate(
            sp=Max('subject_marks')).get('sp', '0')
        context['sub_avg_number'] = std_gpa.marks_set.all().aggregate(
            sp=Avg('subject_marks')).get('sp', '0')
        context['subject_min_number'] = std_gpa.marks_set.all().aggregate(
            sp=Min('subject_marks')).get('sp', '0')


        context['ranks']=Rank.objects.get(std=std_gpa)

        

        
        subject_grade= ((std_gpa.marks_set.filter(
            subject_gradepoint__gte=1).aggregate(sp=Sum('subject_gradepoint')).get('sp', 0)))

        total_marks = ((std_gpa.marks_set.all().aggregate(
            sp=Sum('subject_marks')).get('sp', 0)))



        if subject_grade == None or total_marks == None:
            context['toatal_grade_point'] = 0
            context['total_marks'] = 0
        else:
            if int(std_gpa.std_class) == 6 or int(std_gpa.std_class) == 7 :

                context['toatal_grade_point'] = subject_grade/7
                context['total_marks'] = total_marks

            elif int(std_gpa.std_class) == 8:
                context['toatal_grade_point'] = subject_grade/7
                context['total_marks'] = total_marks

            elif int(std_gpa.std_class) == 9 or int(std_gpa.std_class) == 10:
                context['toatal_grade_point'] = subject_grade/9
                context['total_marks'] = total_marks

        


        context['fail'] = failed
        
        

        return context


class StudentAdd(LoginRequiredMixin, CreateView):

    form_class = AddStudentInfo

    template_name='results/std_add.html'

    success_url = reverse_lazy('std_add')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(StudentAdd, self).get_context_data(**kwargs)
        context['std_all']=StudentInfo.objects.all().order_by('-pub_date')
        
        return context


from django.forms import inlineformset_factory


class StudentUpdateView(LoginRequiredMixin, UpdateView, FormMixin):
    
    model=StudentInfo

    fields = ("__all__")
    template_name = 'results/std_update.html'

    success_url = reverse_lazy('std_add')
    login_url = 'login'

    
    def get_context_data(self, **kwargs):
        std_pk=self.kwargs['pk']
        std=StudentInfo.objects.get(pk=std_pk)
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['marks']=std.marks_set.all()
        context['newForm'] = StudentSubjectGPAFormAdd()
        return context
    

class StudentAddmarks(TemplateView):
    template_name='results/std_add_marks.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAddmarks, self).get_context_data(**kwargs)
        context['newForm'] = Addmarks()
        return context


from django.forms import modelformset_factory
from django.forms import inlineformset_factory


@login_required
def student_add_marks(request, pk):

    std=StudentInfo.objects.get(pk=pk)

    AuthorFormSet = inlineformset_factory(
        StudentInfo, Marks, fields=('subject_name', 'subject_marks',), fk_name='std_name', extra=30)

   

    if request.method == 'POST':
        formset = AuthorFormSet(request.POST, request.FILES, instance=std)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = AuthorFormSet()
            
    return render(request, 'results/std_add_marks_func.html', {'form': formset, 'std': std})


class ResultUpdate(LoginRequiredMixin, UpdateView):

    model = StudentInfo
    template_name = 'results/std_marks_update.html'
    fields = ['std_name']
    login_url = 'login'  # new
    


    
    def get_context_data(self, **kwargs):
        context = super(ResultUpdate, self).get_context_data(**kwargs)
        #context['']=
        return context
    

class Pdf(DetailView):
    model=StudentInfo

    failed = 0
    same_subject = []

    def get(self, request, pk):
        failed = 0
        same_subject = []
        try:
            std = StudentInfo.objects.get(pk=pk)
            ranks = Rank.objects.get(std=std)
            today = timezone.now()

            std_gpa = std

            for i in std_gpa.marks_set.filter(subject_name__subject_type__startswith='R').order_by('-pub_date'):

                if i.subject_name not in same_subject:
                    same_subject.append(i.subject_name)
                    if i.subject_gpa == 'F':
                        failed = failed+1

            subject_max_number = std_gpa.marks_set.all().aggregate(
                sp=Max('subject_marks')).get('sp', '0')
            sub_avg_number = std_gpa.marks_set.all().aggregate(
                sp=Avg('subject_marks')).get('sp', '0')
            subject_min_number = std_gpa.marks_set.all().aggregate(
                sp=Min('subject_marks')).get('sp', '0')

            ranks = Rank.objects.get(std=std_gpa)

            subject_grade = ((std_gpa.marks_set.filter(
                subject_gradepoint__gte=1).aggregate(sp=Sum('subject_gradepoint')).get('sp', 0)))

            total_marks = ((std_gpa.marks_set.all().aggregate(
                sp=Sum('subject_marks')).get('sp', 0)))

            if subject_grade == None or total_marks == None:
                toatal_grade_point = 0
                total_marks = 0
            else:
                if int(std_gpa.std_class) == 6 or int(std_gpa.std_class) == 7:

                    toatal_grade_point = subject_grade/7
                    total_marks = total_marks

                elif int(std_gpa.std_class) == 8:
                    toatal_grade_point = subject_grade/7
                    total_marks = total_marks

                elif int(std_gpa.std_class) == 9 or int(std_gpa.std_class) == 10:
                    toatal_grade_point = subject_grade/9
                    total_marks = total_marks

            fail = failed
            time=timezone.now()

            params = {
                'today': today,
                'object': std,
                'request': request,
                'ranks': ranks,
                'subject_min_number': subject_min_number,
                'sub_avg_number': sub_avg_number,
                'subject_max_number': subject_max_number,
                'total_marks': total_marks,
                'fail': fail,
                'toatal_grade_point': toatal_grade_point,
                'time':time,

            }
        
        except:
            params={
                'object': 'Problem',
            }
        return Render.render('results/pdf.html', params)


class RankListView(ListView):
    model=Rank
    template_name="results/rank_list.html"


    
    def get_context_data(self, **kwargs):
        
        context = super(RankListView, self).get_context_data(**kwargs)
        context['object_list'] = Rank.objects.all().order_by('school_rank')
        context['rank_count'] = Rank.objects.all().count()
        return context
    

class SubjectSeaechView(TemplateView, FormMixin):
    template_name = 'results/subject_seach.html'

    form_class = SubjectSearchForm

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = self.form_class(request.POST)
        if form.is_valid():

            try:
                self.object_search = StdSubject.objects.get(
                    subject_form_searh_name=form.cleaned_data['subject_name'], subjet_class=form.cleaned_data['subject_class'])
                context['std_search_count'] = self.object_search.marks_set.all().count()
            except:
                self.object_search = False
                context['std_search_count'] =False
                
           
            

            
           
        context['std_search'] = self.object_search
        

        

        #context['ranks'] = Rank.objects.get(std=self.object_search)
        #self.object_search.marks

        return super(SubjectSeaechView, self).render_to_response(context)




class SubjectDetailView(DetailView):
    model=StdSubject
    template_name = 'results/subject_details.html'



    
    def get_context_data(self, **kwargs):
        context = super(SubjectDetailView, self).get_context_data(**kwargs)
        subject_id = self.kwargs['pk']
        sub_object=StdSubject.objects.get(pk=subject_id)
        context['sub_std'] = sub_object.marks_set.all().order_by(
            '-subject_gradepoint')
        context['sub_std_count'] = sub_object.marks_set.all().order_by(
            '-subject_gradepoint').count()
        context['sub_std_pass'] = sub_object.marks_set.filter(
            subject_gradepoint__gte=1).order_by('-subject_gradepoint').count()
        context['sub_std_fail'] = sub_object.marks_set.filter(subject_gradepoint__lte=0).order_by('-subject_gradepoint').count()

        context['sub_std_aplus'] = sub_object.marks_set.filter(
            subject_gradepoint__gte=5).order_by('-subject_gradepoint').count()
        context['sub_std_a'] = sub_object.marks_set.filter(
            subject_gradepoint__gte=4, subject_gradepoint__lt=5).order_by('-subject_gradepoint').count()

        context['sub_std_aminus'] = sub_object.marks_set.filter(
            subject_gradepoint__gte=3.5, subject_gradepoint__lt=4).order_by('-subject_gradepoint').count()
        context['sub_std_b'] = sub_object.marks_set.filter(
            subject_gradepoint__gte=3, subject_gradepoint__lt=3.5).order_by('-subject_gradepoint').count()

        context['sub_std_c'] = sub_object.marks_set.filter(
            subject_gradepoint__gte=2, subject_gradepoint__lt=3).order_by('-subject_gradepoint').count()
        context['sub_std_d'] = sub_object.marks_set.filter(
            subject_gradepoint__gte=1, subject_gradepoint__lt=2).order_by('-subject_gradepoint').count()

        context['sub_avg_marks'] = sub_object.marks_set.all().aggregate(
            sp=Avg('subject_marks')).get('sp', '0')
        context['sub_avg_gradepoint'] = sub_object.marks_set.all().aggregate(
            sp=Avg('subject_gradepoint')).get('sp', '0')
        return context
    

class AllRankViewSearch(TemplateView,FormMixin):

    form_class = ClassSearchForm

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = self.form_class(request.POST)
        if form.is_valid():

            try:
                self.object_search = StudentInfo.objects.filter(
                    std_class=form.cleaned_data['student_class'])
                context['class_name']=form.cleaned_data['student_class']
                context['std_search_count'] = self.object_search.count()

                
                
            except:
                self.object_search = False
                context['std_search_count'] = False

        context['std_search'] = self.object_search.order_by('-std_grade_point_total_subject_avg')

        #context['ranks'] = Rank.objects.get(std=self.object_search)
        #self.object_search.marks

        return super(AllRankViewSearch, self).render_to_response(context)


