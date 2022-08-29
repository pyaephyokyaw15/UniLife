from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('comments', views.CommentViewSet)
router.register('accounts', views.UserViewSet)


urlpatterns = [
    # starts with api/v2/
    path('', include(router.urls)),
    path('auth/token/', views.TokenView.as_view(), name='token'),
    path('auth/register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('posts/<int:pk>/save/', views.PostSaveActionAPIView.as_view(), name='post-save'),
    path('posts/<int:pk>/like/', views.PostLikeActionAPIView.as_view(), name='post-like'),
    path('accounts/<int:pk>/follow/', views.FollowAPIView.as_view(), name='user-follow'),
]
