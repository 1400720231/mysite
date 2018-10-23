from django.contrib import admin
from .models import BlogArtciles
# Register your models here.


class BlogArtcilesAdmin(admin.ModelAdmin):
	list_display = ('title','author','publish')
	search_display = ('title','author')
	list_filter = ('title','author','publish')
	raw_id = ('author')
	date_hierarchy = 'publish'
	ordering = ['publish','author']

admin.site.register(BlogArtciles, BlogArtcilesAdmin)