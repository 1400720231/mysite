from django.conf.urls import url, include
from django.contrib import admin
from .views import user_login,user_logout,register,reset_password,modify_password

urlpatterns = [
    url(r'^login/$', user_login, name="user_login"),
    url(r'^logout/$', user_logout, name="user_logout"),
    url(r'^register/$', register, name="user_register"),
    url(r'^modify_pw/$',modify_password, name="modify_password"),
    url(r'^reset/$',reset_password, name="reset_password"),
 
    
]
