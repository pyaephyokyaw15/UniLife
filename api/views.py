import rest_framework.renderers
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, viewsets, mixins
from .serializers import PostSerializer, CustomAuthTokenSerializer, UserRegisterSerializer, \
    UserInfoSerializer, PostDetailSerializer, CommentSerializer, UserProfileSerializer,\
    PostCreateSerializer, CommentCreateSerializer, CommentUpdateSerializer
from post.models import Post, Comment
from .permission import IsOwnerOrReadOnly, IsUserOrReadOnly
from .renderers import CustomApiRenderer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser,JSONParser, FileUploadParser

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
@method_decorator(name='list', decorator=swagger_auto_schema(responses={200: ''}))
@method_decorator(name='create', decorator=swagger_auto_schema(responses={201: ''}, request_body=PostCreateSerializer))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(responses={200: ''}))
@method_decorator(name='update', decorator=swagger_auto_schema(responses={200: ''}, request_body=PostCreateSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(responses={200: ''}))
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return PostDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        """Filter the default query_set according to the request parameter"""
        queryset = self.queryset
        print(self.request.query_params)
        # get key from url query parameter
        saved = self.request.query_params.get("is_saved")
        print(saved)
        following = self.request.query_params.get("is_following")
        print(following)
        username = self.request.query_params.get("username")
        print(username)
        q = self.request.query_params.get("q")

        if saved == "true":
            print("Saved posts")
            if self.request.user.is_authenticated:
                queryset = queryset.filter(saved_by=self.request.user)
            else:
                queryset = []

        if username:
            queryset = queryset.filter(owner__username=username)

        if following == "true":
            if self.request.user.is_authenticated:
                queryset = queryset.filter(owner__in=self.request.user.following.all())
            else:
                queryset = []

        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(owner__username__icontains=q) | Q(content__icontains=q))

        return queryset

    def destroy(self, request, *args, **kwargs):
        # override the delete method to get the required status_code(200)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


@method_decorator(name='list', decorator=swagger_auto_schema(responses={200: ''}))
@method_decorator(name='create', decorator=swagger_auto_schema(responses={201: ''}, request_body=CommentCreateSerializer))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(responses={200: ''}))
@method_decorator(name='update', decorator=swagger_auto_schema(responses={200: ''}, request_body=CommentCreateSerializer))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(responses={200: ''}))
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """Filter the default query_set according to the request parameter"""
        queryset = self.queryset

        # get key from url query parameter
        post_id = self.request.query_params.get("post_id")
        if post_id:  # get a certain post's comments
            queryset = queryset.filter(post=post_id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        # override the delete method to get the required status_code(200)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

@method_decorator(name='list', decorator=swagger_auto_schema(responses={200: ''}))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(responses={200: ''}))
@method_decorator(name='update', decorator=swagger_auto_schema(responses={200: ''}))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserOrReadOnly]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'update':
            return UserInfoSerializer
        return self.serializer_class


class TokenView(ObtainAuthToken):
    # POST api/v2/auth/token/
    renderer_classes = [CustomApiRenderer]
    serializer_class = CustomAuthTokenSerializer

    # generate token
    @swagger_auto_schema(responses={200: ''})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserInfoSerializer(user).data,
            "token": token.key
        })

    @swagger_auto_schema(responses={200: ''})
    def delete(self, request):
        # not found in documentation(as far as I searched)
        # Checking User and Token Table. It is one-to-one relationship.
        request.user.auth_token.delete()  # simply delete the token to force a login
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        # dynamically change the permission classes according to the request METHOD.

        # To delete token , the user must be authenticated(must have token).
        if self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class UserRegisterAPIView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(responses={200: ''})
    def post(self, request, *args, **kwargs):
        print('Request Data', request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        user = serializer.save()
        print(user)
        print(user.password)

        # create token and return this token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserInfoSerializer(user).data,
            "token": token.key
        })


class PostSaveActionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [rest_framework.renderers.JSONRenderer]

    @swagger_auto_schema(responses={200: ''})
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)

        # toggle save status
        if post in request.user.saved_posts.all():
            request.user.saved_posts.remove(post)
            return Response({"result": None, "status_code": status.HTTP_200_OK, "message": "unsaved"}, status=status.HTTP_200_OK)
        else:
            request.user.saved_posts.add(post)
            return Response({"result": None, "status_code": status.HTTP_200_OK, "message": "saved"}, status=status.HTTP_200_OK)


class PostLikeActionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [rest_framework.renderers.JSONRenderer]

    @swagger_auto_schema(responses={200: ''})
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)

        # toggle like status
        if post in request.user.liked_posts.all():
            request.user.liked_posts.remove(post)
            return Response({"result": None, "status_code": status.HTTP_200_OK, "message": "unliked"}, status=status.HTTP_200_OK)
        else:
            request.user.liked_posts.add(post)
            return Response({"result": None, "status-code": status.HTTP_200_OK, "message": "liked"}, status=status.HTTP_200_OK)


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [rest_framework.renderers.JSONRenderer]

    @swagger_auto_schema(responses={200: ''})
    def post(self, request, *args, **kwargs):
        current_user = request.user  # login-user
        pk = kwargs['pk']
        profile_user = get_object_or_404(User, pk=pk)  # currently viewing profile-user

        # toggle follow status
        if current_user in profile_user.followers.all():
            profile_user.followers.remove(current_user)
            return Response({"result": None, "status_code": status.HTTP_200_OK, "message": "unfollowed"},
                            status=status.HTTP_200_OK)
        else:
            profile_user.followers.add(current_user)
            return Response({"result": None, "status-code": status.HTTP_200_OK, "message": "followed"},
                            status=status.HTTP_200_OK)


