from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
	STATUS_CHOICES = (
		('published', 'Published'),
		('draft', 'Draft'),
	)

	title = models.CharField(max_length=255)
	owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
	slug = models.SlugField(max_length=255, unique=True)
	category = models.CharField(max_length=120)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
	author = models.CharField(max_length=120)
	date = models.CharField(max_length=50)
	read_time = models.CharField(max_length=50)
	content = models.TextField(blank=True, default='')
	meta_title = models.CharField(max_length=255)
	meta_description = models.TextField()
	h1 = models.CharField(max_length=255)
	alt_text = models.CharField(max_length=255)
	views = models.PositiveIntegerField(default=0)
	image = models.URLField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.title
