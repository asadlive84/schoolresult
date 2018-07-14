from django.contrib import admin

from results.models import StudentInfo, StdSubject, Marks, Rank, SubjectTecher




class RankInstanceInline(admin.TabularInline):
    model=Rank
    fk_name='std'
    extra=0


class SubjectInstanceInline(admin.TabularInline):
    model = Marks
    fk_name = 'std_name'
    extra = 8

    exclude = ['subject_gradepoint', 'subject_gpa']


class SubjectInstance(admin.TabularInline):
    model = StdSubject
    fk_name = 'teacher'
    extra = 8
    exclude = ['subject_form_searh_name']



@admin.register(StudentInfo)
class StudentAdmin(admin.ModelAdmin):
    list_filter = ('std_class', 'std_gender', 'std_group')
    list_display=('std_name','std_class','std_roll','std_group','std_gender')
    inlines = [RankInstanceInline, SubjectInstanceInline]

    
    search_fields = ('std_name','std_roll','std_group')

    exclude = ['std_total_marks', 'std_gpa',
               'std_grade_point_total_sum', 'std_grade_point_total_subject_avg', 'std_fail_subject', 'school_rank','class_rank']

    







@admin.register(StdSubject)
class SubjectModelAdmin(admin.ModelAdmin):
    list_filter = ('subjet_class', 'subject_type')
    list_display = ('subject_name', 'subjet_class',
                    'subject_type', 'subject_full_marks')

    search_fields = ('subject_name', 'subject_code')










@admin.register(SubjectTecher)
class SubjectTecherModel(admin.ModelAdmin):
    list_filter = ('teacher_name','teach_phone_number')
    search_fields = ('teacher_name', 'teach_phone_number')
    
    inlines = [SubjectInstance]


