from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'status', 'author', 'views', 'updated_at')
	search_fields = ('title', 'slug', 'author', 'category')
	list_filter = ('status', 'category')
