from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.home, name='post-home'),
    path('post/', views.PostListView.as_view(), name='posts')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # to get media via url
