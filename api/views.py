from rest_framework import authentication, generics, permissions
# from rest_framework.renderers import JSONRenderer
from .serializers import PostSerializer, CustomAuthTokenSerializer, UserRegisterSerializer, UserInfoSerializer
from post.models import Post
# from django.contrib.auth.models import User
from rest_framework.response import Response
from .permission import UserPostPermissions
from .renderers import CustomApiRenderer
from rest_framework.authtoken.views import ObtainAuthToken  # obtain_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class PostListAPIView(generics.ListAPIView):
    # GET /api/post/list/
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    # def list(self, request, *args, **kwargs):
    #     # you can override this method to get the required api response instead of custom renderer.
    #     response = super().list(request, *args, **kwargs)
    #     custom_response = dict()
    #     custom_response["result"] = {"data": response.data}
    #     custom_response["status_code"] = 200
    #     custom_response["message"] = 'OK'
    #     return Response(custom_response)


class UserPostListAPIView(generics.ListAPIView):
    # GET /api/user/<int:pk>/posts/
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):  # override the method
        user = self.kwargs.get('pk')
        # owner = User.objects.get(id=)
        qs = super().get_queryset()
        return qs.filter(author=user)


class SavedPostListAPIView(generics.ListAPIView):
    # GET /api/user/<int:pk>/posts/
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # override the method

        qs = super().get_queryset()
        return qs.filter(saved_by=self.request.user)


class PostDetailAPIView(generics.RetrieveAPIView):
    # GET /api/post/<int:pk>
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
    # POST /api/post/create/
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
    # PUT /api/post/<int:pk>/update/
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
    # DELETE api/products/<int:pk>/delete/
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # lookup_field = 'pk'
    permission_classes = [UserPostPermissions]


class CreateTokenView(ObtainAuthToken):  # Override the default ObtainAuthToken
    # POST api/auth/token/
    renderer_classes = [CustomApiRenderer]
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            # "user": UserInfoSerializer(user, context=self.get_serializer_context()).data,
            "user": UserInfoSerializer(user).data,
            "token": token.key
        })




class UserRegisterAPIView(generics.GenericAPIView):
    # POST api/auth/register
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        # print('Request Data', request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        user = serializer.save()
        print(user)
        print(user.password)
        token, created = Token.objects.get_or_create(user=user)


        return Response({
            # "user": UserInfoSerializer(user, context=self.get_serializer_context()).data,
            "user": UserInfoSerializer(user).data,
            "token": token.key
        })




class LogoutAPIView(APIView):
    def get(self, request):
        # not found in documentation
        # Checking User and Token Table. It is one-to-one relationship.
        request.user.auth_token.delete()  # simply delete the token to force a login
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostSaveActionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = Post.objects.get(pk=pk)

        if post in request.user.saved_posts.all():
            request.user.saved_posts.remove(post)
            return Response({"state": "unsaved"}, status=status.HTTP_200_OK)
        else:
            request.user.saved_posts.add(post)
            return Response({"state": "saved"}, status=status.HTTP_200_OK)


class PostLikeActionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = Post.objects.get(pk=pk)

        if post in request.user.liked_posts.all():
            request.user.liked_posts.remove(post)
            return Response({"state": "unliked"}, status=status.HTTP_200_OK)
        else:
            request.user.liked_posts.add(post)
            return Response({"state": "liked"}, status=status.HTTP_200_OK)

