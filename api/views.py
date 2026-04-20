from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer, UserSerializer


class IsAdminOrBlogCreator(permissions.BasePermission):
	def has_permission(self, request, view):
		user = request.user
		return bool(
			user
			and user.is_authenticated
			and (user.is_staff or user.groups.filter(name='blog_creator').exists())
		)

	def has_object_permission(self, request, view, obj):
		user = request.user
		if not user or not user.is_authenticated:
			return False
		if user.is_staff:
			return True
		return obj.owner_id == user.id


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def _can_manage_posts(self, user):
		return bool(user and user.is_authenticated and (user.is_staff or user.groups.filter(name='blog_creator').exists()))

	def get_queryset(self):
		user = self.request.user
		scope = self.request.query_params.get('scope')

		if self.action == 'list':
			if scope == 'dashboard' and self._can_manage_posts(user):
				if user.is_staff:
					return Post.objects.all()
				return Post.objects.filter(owner=user)
			return Post.objects.filter(status='published')

		if user.is_staff:
			return Post.objects.all()
		if self._can_manage_posts(user):
			return Post.objects.filter(Q(status='published') | Q(owner=user))
		return Post.objects.filter(status='published')

	def get_permissions(self):
		if self.action in ['list', 'retrieve']:
			return [permissions.AllowAny()]
		return [IsAdminOrBlogCreator()]

	def perform_create(self, serializer):
		user = self.request.user
		if user and user.is_authenticated:
			serializer.save(owner=user)
			return
		serializer.save()


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAdminUser]

	http_method_names = ['get', 'post', 'patch', 'delete']


class MeView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		is_admin = request.user.is_staff
		can_manage_posts = is_admin or request.user.groups.filter(name='blog_creator').exists()
		return Response(
			{
				'id': request.user.id,
				'username': request.user.username,
				'email': request.user.email,
				'is_staff': is_admin,
				'role': 'admin' if is_admin else 'blog_creator' if can_manage_posts else 'viewer',
				'can_manage_users': is_admin,
				'can_manage_posts': can_manage_posts,
			}
		)
