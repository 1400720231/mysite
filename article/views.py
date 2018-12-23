from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# Create your views here.
from .models import ArticleColumn
from .forms import ArticleColumnForm

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
			