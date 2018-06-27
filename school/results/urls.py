from .views import Homepage
from django.urls import path,re_path
from .views import StudentDetails
urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    re_path(r'^(?P<pk>\d+)/$', StudentDetails.as_view(), name='std_details'),
]