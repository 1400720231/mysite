from django.conf.urls import url, include
from django.contrib import admin
from . import  views

urlpatterns = [
    url(r'^$', views.blog_title, name="blog_title"),
    url(r'(?P<article_id>\d)/$', views.blog_detail, name="blog_detail"),
    
]
