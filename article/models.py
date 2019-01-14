from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import User

from slugify import slugify
# 文章主题栏目数据模型
class ArticleColumn(models.Model):
	user = models.ForeignKey(User, related_name="article_column")
	column = models.CharField(max_length=200)
	created = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.column


# 文章内容数据模型
class ArticlePost(models.Model):
	"""
	auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
	auto_now_add为添加时的时间，更新对象时不会有变动。

	"""
	author = models.ForeignKey(User, related_name="article")
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=500)
	column = models.ForeignKey(ArticleColumn, related_name="article_column")
	body = models.TextField()
	created = models.DateTimeField(default=timezone.now())
	updated = models.DateTimeField(auto_now=True)
	# 点赞字段　多对多
	users_like = models.ManyToManyField(User, related_name="article_likes", blank=True)
	class Meta:
		ordering = ("-updated",)
		# 联合索引，表示当查询条件中同时有id slug的时候速度快很多
		index_together = (("id","slug"),)

	def __str__(self):
		return self.title

	def save(self,*args,**kargs):
		self.slug = slugify(self.title)
		super(ArticlePost,self).save(*args, **kargs)

	# 自定义一个属性，获取类似这样的路径：article/article_detail/1/python-study
	def get_absolute_url(self):
		return reverse("article:article_detail", args=[self.id, self.slug])

	# 自定义一个属性和上面是一样的意义，这个是为无权限的所有用户可以访问的编写的
	def get_url_path(self):
		return reverse("article:list_article_detail", args=[self.id, self.slug])



#　文章评论

class Comment(models.Model):
	article = models.ForeignKey(ArticlePost, related_name="comments")
	commentator = models.CharField(max_length=80)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ("-created",)


	def __str__(self):
		return "Comment by {0} on {1}".format(self.commentator.username,self.article)