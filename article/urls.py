from django.conf.urls import url, include
from . import views


urlpatterns = [
	# 增加
    url(r'^article-column/$', views.article_column, name="article_column"),
    # 重命名
    url(r'^rename-column/$', views.rename_article_column, name="rename_article_column"),
    # 删除
    url(r'^del-column/$', views.del_article_column, name="del_article_column"),
    
]
