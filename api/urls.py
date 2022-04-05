from django.urls import path
from . import views

urlpatterns = [
    path('post/list/', views.PostListAPIView.as_view(), name='api-post-list'),
    # path('<my>/post/list/', views.UserPostListAPIView.as_view(), name='api-user-post-list'),
    path('<int:user_id>/post/list/', views.UserPostListAPIView.as_view(), name='api-user-post-list'),
    path('post/<int:pk>/', views.PostDetailAPIView.as_view(), name='api-post-detail'),
    path('post/create/', views.PostCreateAPIView.as_view(), name='api-post-create'),
    path('post/<int:pk>/update/', views.PostUpdateAPIView.as_view(), name='api-post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteAPIView.as_view(), name='api-post-delete'),
]

