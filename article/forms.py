from django import forms
from .models import ArticleColumn, ArticlePost,Comment

# 主题栏目表单
class ArticleColumnForm(forms.ModelForm):
	class Meta:
		model = ArticleColumn
		fields = ("column",)


# 文章内容表单

class ArticlePostForm(forms.ModelForm):
	class Meta:
		model = ArticlePost
		fields = ("title", "body")


# 评论表单

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ("commentator","body",)