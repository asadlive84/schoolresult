"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from results.views import Homepage, RankListView
from results.api.views import UserViewSet
from django.contrib.auth import views as auth_views

from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

#router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)





#from django.contrib.auth import login
#from django.contrib.auth import authenticate, login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Homepage.as_view(), name='home_app'),
    path('results/', include('results.urls')),
    #path('login/', auth_views.login, name='login1'),
    path('results/', include('django.contrib.auth.urls')),
    path('api/', UserViewSet.as_view(), name='api'),
    #re_path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    path('all-school-rank.php/',RankListView.as_view() , name='rank'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
school_name = 'Fulhata Secondary School'

# default: "Django Administration"
admin.site.site_header = school_name+' Admin Panel'
# default: "Site administration"
admin.site.index_title = school_name+' Administration '
admin.site.site_title = school_name+' adminsitration'
