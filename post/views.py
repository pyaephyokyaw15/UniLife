from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Post


# Create your views here.
def home(request):
    # /
    return HttpResponse('Hello')


class PostListView(ListView):
    # /post/
    model = Post
    # template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    # context_object_name = 'posts'

    # ordering = ['-date_posted']
    # paginate_by = 2