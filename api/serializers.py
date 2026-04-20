from rest_framework import serializers
from django.contrib.auth.models import Group, User

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    ownerId = serializers.IntegerField(source='owner_id', read_only=True)
    readTime = serializers.CharField(source='read_time', required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True)
    metaTitle = serializers.CharField(source='meta_title', required=False, allow_blank=True)
    metaDescription = serializers.CharField(
        source='meta_description', required=False, allow_blank=True
    )
    altText = serializers.CharField(source='alt_text')

    class Meta:
        model = Post
        extra_kwargs = {
            'author': {'required': False, 'allow_blank': True},
            'content': {'required': False, 'allow_blank': True},
        }
        fields = [
            'id',
            'ownerId',
            'title',
            'slug',
            'category',
            'status',
            'author',
            'date',
            'readTime',
            'content',
            'metaTitle',
            'metaDescription',
            'h1',
            'altText',
            'views',
            'image',
            'created_at',
            'updated_at',
        ]

    def _default_author(self):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return user.get_full_name() or user.username
        return ''

    def create(self, validated_data):
        if not validated_data.get('author'):
            validated_data['author'] = self._default_author()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'author' in validated_data and not validated_data.get('author'):
            validated_data['author'] = self._default_author() or instance.author
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = ('admin', 'blog_creator')

    password = serializers.CharField(write_only=True, min_length=8, required=False)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False, default='blog_creator')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'is_staff']

    def _apply_role(self, user: User, role: str):
        blog_group, _ = Group.objects.get_or_create(name='blog_creator')
        if user.pk:
            user.groups.remove(blog_group)

        if role == 'admin':
            user.is_staff = True
        else:
            user.is_staff = False
            user.is_superuser = False
            if user.pk:
                user.groups.add(blog_group)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['role'] = 'admin' if instance.is_staff else 'blog_creator'
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})
        role = validated_data.pop('role', 'blog_creator')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        self._apply_role(user, role)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        if role:
            self._apply_role(instance, role)

        instance.save()
        return instance
