from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'
urlpatterns = [
    # starts with api/
    path('auth/token/', views.CreateTokenView.as_view(), name='create-token'),
    path('auth/register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('post/list/', views.PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateAPIView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateAPIView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteAPIView.as_view(), name='post-delete'),
    path('user/<int:pk>/posts/', views.UserPostListAPIView.as_view(), name='user-post-list'),
    path('auth/logout/', views.Logout.as_view()),
]

