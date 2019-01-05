from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# Create your views here.
from .models import ArticleColumn,ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# 栏目增加视图函数
@login_required(login_url='/account/login/')
# 解决post的跨域的问题的装饰器
@csrf_exempt
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        context = {"columns":columns, "column_form":column_form}
        return render(request, "article/column/article_column.html", context=context)
    if request.method == "POST":
        column_name = request.POST["column"]
        columns = ArticleColumn.objects.filter(user=request.user,column=column_name)
        # 如果存在该栏目，就返回1给ajax,否则返回2
        if columns:
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse("1")

# 栏目重命名视图函数
@login_required(login_url='/account/login/')
@csrf_exempt
def rename_article_column(request):
    if request.method == 'POST':
        column_name = request.POST["column_name"]
        column_id = request.POST["column_id"]
        try:
            line = ArticleColumn.objects.get(id=column_id)
            line.column = column_name
            line.save()
            return HttpResponse("1")
        except:
            return HttpResponse("0")

# 删除栏目视图函数
@login_required(login_url='/account/login/')
@csrf_exempt
def del_article_column(request):
    if request.method == 'POST':
        column_id = request.POST.get("column_id")
        try:
            line = ArticleColumn.objects.get(id=column_id)
            line.delete()
            return HttpResponse("1")
        except:
            return HttpResponse("2")
            

# 添加文章的视图函数
@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method=="POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                # tags = request.POST['tags']
                # if tags:
                #     for atag in json.loads(tags):
                #         tag = request.user.tag.get(tag=atag) 
                #         new_article.article_tag.add(tag) 

                
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all() 
        # article_tags = request.user.tag.all()
        
        context  ={"article_post_form":article_post_form, 
                "article_columns":article_columns}
        return render(request, "article/column/article_post.html",context=context )



"""
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    objects = ['john', 'edward', 'josh', 'frank']

    # Provide Paginator with the request object for complete querystring generation

    p = Paginator(objects, request=request)

    people = p.page(page)

    return render_to_response('index.html', {
        'people': people,
    }

"""
# 文章列表
# 第三方分页文档：https://github.com/jamespacileo/django-pure-pagination
# 需要注意的是在html长中迭代的时要这样：for i in articles.object_list
@login_required(login_url="/account/login/")
def article_list(request):
    articles = ArticlePost.objects.filter(author =request.user)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    # 需要注意的是这里的１０原文档是没有的，表示一页几个数据
    p = Paginator(articles,10, request=request)

    people = p.page(page)

    return render(request, "article/column/article_list.html",{"articles":people})

# 文章详情

@login_required(login_url="/account/login/")
def article_detail(request,id,slug):
    if request.method == "GET":
        article = get_object_or_404(ArticlePost,id=id, slug=slug)
        return render(request, "article/column/article_detail.html",{"article":article})

# 删除文章
@login_required(login_url="/account/login/")
@csrf_exempt
def del_article(request):
    article_id = request.POST["article_id"]
    if request.method =="POST":
        try:
            article = ArticlePost.objects.get(id = article_id)
            article.delete()
            return HttpResponse("1")
        except:
            return HttpResponse("2")


# 修改文章
@login_required(login_url="/account/login/")
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id = article_id)
        # 这里的instance参数一定要加，不然modelform不晓得是哪个instance,或者你不用instance这
        # 中方法，用initial={"title":xxx}这种也行
        this_article_form = ArticlePostForm(instance=article)
        this_article_column = article.column
        context = {"article": article,
                    "article_columns": article_columns,
                    "this_article_column": this_article_column,
                    "this_article_form": this_article_form}
        return render(request, "article/column/redit_article.html",context=context)
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST["column_id"])
            redit_article.title = request.POST["title"]
            redit_article.body = request.POST["body"]
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2") 

# 文章标题们

def article_titles(request):
    aricle_titles = ArticlePost.objects.all()

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    # 需要注意的是这里的１０原文档是没有的，表示一页几个数据
    p = Paginator(aricle_titles ,10, request=request)

    people = p.page(page)
    return render(request, "aricle/list/article_titles.html", context={"article_titles":people})