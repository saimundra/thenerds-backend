from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import MeView, PostViewSet, UserViewSet

router = DefaultRouter(trailing_slash='/?')
router.register('posts', PostViewSet, basename='posts')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # Accept both slash and no-slash variants to avoid POST redirect issues
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair_no_slash'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh_no_slash'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me', MeView.as_view(), name='auth_me_no_slash'),
    path('auth/me/', MeView.as_view(), name='auth_me'),
    # Mirror viewset endpoints without trailing slash for proxy setups that trim '/'.
    path(
        'users',
        UserViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='users_no_slash',
    ),
    path(
        'users/<int:pk>',
        UserViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='users_detail_no_slash',
    ),
    path(
        'posts',
        PostViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='posts_no_slash',
    ),
    path(
        'posts/<int:pk>',
        PostViewSet.as_view(
            {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
        name='posts_detail_no_slash',
    ),
    path('', include(router.urls)),
]