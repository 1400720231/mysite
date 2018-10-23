from django.shortcuts import render, get_object_or_404

from .models import BlogArtciles
# Create your views here.


def blog_title(request):
    blogs = BlogArtciles.objects.all()
    context = {'blogs':blogs}
    return render(request, 'blog/titles.html', context=context)

def blog_detail(request,article_id):
    # article = BlogArtciles.objects.get(id=article_id)
    article = get_object_or_404(BlogArtciles, id=article_id)
    pub = article.publish
    context = {"article": article,'publish':pub}
    return render(request, 'blog/content.html', context=context)