from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse

from .models import ArticleColumn, ArticlePost
from .forms import CommentForm
import redis

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)
# 所有数据库的title函数
def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        article_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        article_title = ArticlePost.objects.all()

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    # 需要注意的是这里的10原文档是没有的，表示一页10个数据
    p = Paginator(article_title,10, request=request)

    people = p.page(page)
    if username:
        return render(request, "article/list/article_titles.html", {"articles":people,"user":user,"userinfo":userinfo})


    return render(request, "article/list/article_titles.html", {"articles":people})



# 所有数据库的title对应的detail函数,和views.py下的函数一模一样，只是没login_rquired限制
"""
redis的incr表示吧key+1并且返回+1后的数字(string类型数据结构)
zincrby(name,value,amount):(zset有序集合数据集类型)
    表示对name的value+amount,这里表示对此时访问数量+1,
r.zrange("article_ranking",0,-1, desc=True)[:10]:
    表示索引article_ranking从0到-1，即全部，desc=True倒叙，[:10]前10个最大阅读数的文章
的id 
"""
def article_detail(request,id,slug):
  
    article = get_object_or_404(ArticlePost,id=id, slug=slug)
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby("article_ranking",article.id, 1)
    article_ranking = r.zrange("article_ranking",0,-1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    # 注意id__in这种用法，多使用多复习
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    # 按照id索引大小排序。。。也就是在数据库中创建的时间。。。。这尼玛
    most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))

    # 评论功能
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, "article/list/article_detail.html",
                    {"article":article,"total_views":total_views,
                    "most_viewed":most_viewed,"comment_form":comment_form})




# 点赞视图函数
@csrf_exempt
@login_required(login_url='/account/login/')
@require_POST
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    print(article_id, action)
    print("哈哈哈")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=int(article_id))
            if action == "like":
                article.users_like.add(request.user)
                
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")
