from django.conf.urls import url, include
from django.contrib import admin
from .views import user_login,user_logout,register,send_reset_password,modify_password,password_reset

urlpatterns = [
    url(r'^login/$', user_login, name="user_login"),
    url(r'^logout/$', user_logout, name="user_logout"),
    url(r'^register/$', register, name="user_register"),
    url(r'^modify_pw/$',modify_password, name="modify_password"),
    url(r'^send_reset/$',send_reset_password, name="send_reset_password"),
    url(r'^reset/(?P<code>.*)/$',password_reset, name="password_reset"),
  	# url(r'^info/(?P<course_id>\d+)/$'
    
]
