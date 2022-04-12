from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='post-home'),
    path('post/', views.PostListView.as_view(), name='posts')
]