from django.contrib import admin
from results.models import StudentInfo, StdSubject, Marks




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
    )




admin.site.register(Marks)
admin.site.register(StdSubject)