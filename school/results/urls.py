from .views import Homepage
from django.urls import path

urlpatterns = [
    url('', Homepage.as_view(), name='home'),
]