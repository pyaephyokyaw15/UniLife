from django.shortcuts import render
from rest_framework import authentication, generics, permissions
from .serializers import PostSerializer
from post.models import Post
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .permission import UserPostPermissions
from .renderers import CustomRenderer


# Create your views here.
class PostListAPIView(generics.ListAPIView):
    # GET /api/post/list/
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    renderer_classes = [CustomRenderer]

    # def list(self, request, *args, **kwargs):
    #     # you can override this method to get the required api response instead of custom renderer.
    #     response = super().list(request, *args, **kwargs)
    #     custom_response = dict()
    #     custom_response["result"] = {"data": response.data}
    #     custom_response["status_code"] = 200
    #     custom_response["message"] = 'OK'
    #     return Response(custom_response)


class UserPostListAPIView(generics.ListAPIView):
    # /api/user/<int:pk>/posts/
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):  # override the method
        user = self.kwargs.get('pk')
        # owner = User.objects.get(id=)
        qs = super().get_queryset()
        return qs.filter(author=user)


class PostDetailAPIView(generics.RetrieveAPIView):
    # /api/post/<int:pk>
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    # def get(self, request, *args, **kwargs):
    #     # you can override this method to get the required api response instead of custom renderer.
    #     response = super().retrieve(request, *args, **kwargs)
    #     custom_response = dict()
    #     print('Data', response.data)
    #     custom_response["result"] = {"data": response.data}
    #     custom_response["status_code"] = 200
    #     custom_response["message"] = 'OK'
    #     return Response(custom_response)


class PostCreateAPIView(generics.CreateAPIView):
    # /api/post/create/
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     # you can override this method to get the required api response instead of custom renderer.
    #     response = super().create(request, *args, **kwargs)
    #     custom_response = dict()
    #     print('Data', response.data)
    #     custom_response["result"] = {"data": response.data}
    #     custom_response["status_code"] = 201
    #     custom_response["message"] = 'Created'
    #     return Response(custom_response, status=status.HTTP_201_CREATED)


class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
    # /api/post/<int:pk>/update/
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # lookup_field = 'pk'
    permission_classes = [UserPostPermissions]

    # def update(self, request, *args, **kwargs):
    #     # you can override this method to get the required api response instead of custom renderer.
    #     response = super().update(request, *args, **kwargs)
    #     custom_response = dict()
    #     print('Data', response.data)
    #     custom_response["result"] = {"data": response.data}
    #     custom_response["status_code"] = 200
    #     custom_response["message"] = 'OK'
    #     return Response(custom_response)


class PostDeleteAPIView(generics.DestroyAPIView):
    # api/products/<int:pk>/delete/
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # lookup_field = 'pk'
    permission_classes = [UserPostPermissions]
