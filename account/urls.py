from django.conf.urls import url, include
from django.contrib import admin
from .views import user_login,user_logout,register

urlpatterns = [
    url(r'^login/$', user_login, name="user_login"),
    url(r'^logout/$', user_logout, name="user_logout"),
    url(r'^register/$', register, name="user_register"),
 
    
]
