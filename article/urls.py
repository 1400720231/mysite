from django.conf.urls import url, include
from . import views


urlpatterns = [
    # 栏目增加
    url(r'^article-column/$', views.article_column, name="article_column"),
    # 栏目重命名
    url(r'^rename-column/$', views.rename_article_column, name="rename_article_column"),
    # 栏目删除
    url(r'^del-column/$', views.del_article_column, name="del_article_column"),
    # 文章添加路由
    url(r'^article-post/$', views.article_post, name="article_post"),
    # 文章列表
    url(r'^article-list/$',views.article_list, name="article_list"),
    # 文章详情
    url(r'^article-detail/(?P<id>\d+)(?P<slug>[-\w]+)$',views.article_detail, name="article_detail"),
    #　编辑文章
    url(r'^redit-article/(?P<article_id>\d+)/$', views.redit_article,name="redit_article"),
    # 删除文章
    url(r'^del-article/$', views.del_article,name="del_article"),
    # 所有标题
    url(r'^article-titles/$', views.article_titles,name="article_titles")
    
]
