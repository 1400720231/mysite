from django import template
from django.db.models import Count
from article.models import ArticlePost
register = template.Library()

#------------------------自定义标签函数------------------------
@register.simple_tag
def total_articles():
	return ArticlePost.objects.count()

# 这个是传参数的标签函数，和普通的传参没什么区别
@register.simple_tag
def author_total_articles(user):
	return user.article.count()


@register.inclusion_tag("article/list/latest_articles.html")
def latest_articles(n=5):
	latest_articles = ArticlePost.objects.order_by("-created")[:n]
	return {"latest_articles":latest_articles}

"""
annotate:标注，注释
意思是先对ArticlePost中所有的文章实例进行标注，标注后的字段为total_commnets,
它的值为Count("commnets"),Count()函数的作用为数queryset对象的实例个数，而这里
的“comments”表示model Comments中的models.ForeignKey(ArticlePost, related_name="comments"),
这的related_name="comments"。总的来说就是求ArticlePost中的每个文章的评论总数，用annotate标记给了
total_comments，每个ArticlePost实例多了一个total_comments属性。
"""
@register.assignment_tag
def most_commented_articles(n=3):
	return ArticlePost.objects.annotate(total_comments=Count("comments")).\
			order_by("-total_comments")[:n]

"""
使用方法：
1、在根目录下新建一个templatetags的文件夹，其中templatetags为固定写法。
2、在templatetags文件夹下新建一个__init__.py,并且新建另一个py文件，比如这里的article_tags.py
3、在导入调用的时候{% load article_tags %}，需要注意的是load的是article_tags.py的名字，不是具体的
	total_articles()函数的名字。

simple_tag:
	返回值是一个字符串，直接调用就行了。先{% load total_articles %},然后再{% total_articles %}就行，
传参方式和django的url传参类似，{% total_articles 3 %}

inclusion_tag:
	返回值是一个模板文件。使用时分２个步骤。
	(1)参数指明模本文件，并且在文件中写你想要的html文件，
		@register.inclusion_tag("article/list/latest_articles.html")
	(2)在目标html文件中调用标签的时候和上面simple_tag方式一样{% latest_articles 4 %}
	强调，强调再强调，一定要分两部执行，特别是第一步中指明模板文件，不然都不晓得是什么乱七八糟的报错。。。
assignment_tag:
	返回一个类似queryset的可迭代对象。之所以说它是类似可迭代，是因为使用的时候必须先赋值。
比如像这样：{% most_commented_articles as commnets%}然后就可以像直接render queryset对象到html
那样使用了：{% for commnet in  commnets%} 
			<p>{{ commnet.title }}</>
"""


#------------------------自定义模板选择器------------------------
from django.utils.safestring import mark_safe
import markdown
@register.filter(name="markdown")
def markdown_filter(text):
	return mark_safe(markdown.markdown(text))

"""
模板选择器:
	name="markdown"表示待会在html中用的时候的名字：{{ article.body | markdown }}
	text参数表示管管道符号“|”前面传入的值，return经过操作后的数据给html.
	其中markdown()把markdown语法渲染成带有html格式的数据给django,但是django不知道这些数据
是否安全，因为这些数据和往常不一样，有些可能是这样：”<p>你好啊</>”，为了让数据给django知道这是安全
的，就调用了mark_safe函数，告诉他这些数据都可以放行，到了前段才能显示成<p>标签渲染会的样子，不然就胡、会
直接显示<p>标签。。。。
"""