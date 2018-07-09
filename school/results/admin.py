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
    
    inlines = [BooksInstanceInline]



admin.site.register(StdSubject)