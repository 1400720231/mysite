from django import forms
from .models import ArticleColumn, ArticlePost

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