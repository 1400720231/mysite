from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# 文章主题栏目数据模型
class ArticleColumn(models.Model):
	user = models.ForeignKey(User, related_name="article_column")
	column = models.CharField(max_length=200)
	created = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.column
