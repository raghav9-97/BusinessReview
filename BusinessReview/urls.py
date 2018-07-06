"""BusinessReview URL Configuration

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
from django.urls import path
from django.contrib.auth import views as auth_views
from collectdata import views as col_views
from collectdata.views import BusiModel
from signup import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('deladmin/',col_views.deladmin,name='Deleteadmin'),
    path('createmanager/',views.createmag,name='CreateManager'),
    path('management/',col_views.management,name='InfoMgmt'),
    path(r'^deletemag/(?P<mag_id>\d+)/$', col_views.delmag, name='delMag'),
    path(r'^updatemag/(?P<bus_id>\d+)/$', col_views.updatemag, name='updateMag'),
    path(r'^deletebusin/(?P<busin_id>\d+)/$', col_views.delbus, name='delBus'),
    path(r'^reviews/(?P<user_id>\d+)/$',col_views.reviews,name='Reviews'),
    path('addbusiness/',col_views.busimodel,name='addbusiness'),
    path('userpage/',views.userpage,name='userpage'),
    path('login/',views.loginuser,name='login'),
    path('logout/',auth_views.logout,{'next_page':'/login'},name='logout'),
    path('signup/',views.signup, name='signup'),
]
