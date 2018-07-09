from .views import Homepage
from django.urls import path,re_path
from .views import StudentDetails, StudentAdd, ResultUpdate, StudentUpdateView, StudentAddmarks, student_add_marks
urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    re_path(r'^(?P<pk>\d+)/$', StudentDetails.as_view(), name='std_details'),

    path('student_add/', StudentAdd.as_view(), name='std_add'),
    re_path(r'student_update/(?P<pk>\d+)/$', StudentUpdateView.as_view(), name='std_update'),

    re_path(r'student_marks_add/(?P<pk>\d+)/$', StudentAddmarks.as_view(), name='std_add_marks'),


    re_path(r"std_add_marks_func/(?P<pk>\d+)/$", student_add_marks, name='stdAdd_marks'),

    re_path(r"std_marks_update/(?P<pk>\d+)/$",ResultUpdate.as_view(), name='stdmarks_update'),

    
]
