from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'
urlpatterns = [
    # starts with api/
    path('auth/token/', views.CreateTokenView.as_view(), name='create-token'),
    path('auth/register/', views.UserRegisterAPIView.as_view(), name='register'),
    path('post/list/', views.PostListAPIView.as_view(), name='post-list'),
    path('saved_post/list/', views.SavedPostListAPIView.as_view(), name='saved-post-list'),
    path('post/<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateAPIView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateAPIView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteAPIView.as_view(), name='post-delete'),
    path('post/<int:pk>/save/', views.PostSaveActionAPIView.as_view(), name='post-save'),
    path('post/<int:pk>/like/', views.PostLikeActionAPIView.as_view(), name='post-like'),

    path('comment/create/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateAPIView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteAPIView.as_view(), name='comment-delete'),
    path('user/<int:pk>/posts/', views.UserPostListAPIView.as_view(), name='user-post-list'),
    path('auth/logout/', views.LogoutAPIView.as_view()),
]

