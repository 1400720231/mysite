from django import forms
from .models import ArticleColumn

# 主题栏目表单
class ArticleColumnForm(forms.ModelForm):
	class Meta:
		model = ArticleColumn
		fields = ("column",)