from django.contrib import admin

from results.models import StudentInfo, StdSubject, Marks


'''

@admin.register(StudentInfo)
class StudentAdmin(admin.ModelAdmin):
    list_display=('std_name','std_roll','std_class')

    fieldsets = (
        ('Student Information', {
            'fields': (
                'std_name',
                'std_roll',
                'std_class',
                
            ),
        }),

        ('Subject Info', {
            'fields': (
                'std_subjects',
                
            ),
        }),

        ('Subject Marks', {
            'fields': (
                'std_name__subject_name',

            ),
        }),
    )

'''
class BooksInstanceInline(admin.TabularInline):
    model = Marks
    fk_name = 'std_name'
    extra = 8


@admin.register(StudentInfo)
class BookAdmin(admin.ModelAdmin):
    list_filter = ('std_class', 'std_gender', 'std_group')
    list_display=('std_name','std_class','std_roll','std_group','std_gender')
    
    inlines = [BooksInstanceInline]
    search_fields = ('std_name','std_roll','std_group')
    






@admin.register(StdSubject)
class SubjectModelAdmin(admin.ModelAdmin):
    list_filter = ('subjet_class', 'subject_type')
    list_display = ('subject_name', 'subjet_class',
                    'subject_type', 'subject_full_marks')

    search_fields = ('subject_name', 'subject_code')






