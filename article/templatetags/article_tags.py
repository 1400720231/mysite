from django import template
from article.models import ArticlePost
register = template.Library()


@register.simple_tag
def total_articles():
	return ArticlePost.objects.count()