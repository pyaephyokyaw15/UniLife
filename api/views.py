import rest_framework.renderers
from rest_framework import authentication, generics, permissions, viewsets, mixins
from rest_framework.renderers import JSONRenderer
from .serializers import PostSerializer, CustomAuthTokenSerializer, UserRegisterSerializer, UserInfoSerializer, PostDetailSerializer, CommentSerializer, UserProfileSerializer
from post.models import Post, Comment
# from django.contrib.auth.models import User
# from rest_framework.response import Response
from .permission import IsOwnerOrReadOnly, IsUserOrReadOnly
from .renderers import CustomApiRenderer
from rest_framework.authtoken.views import ObtainAuthToken  # obtain_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return PostDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        saved = "saved" in self.request.query_params
        following = "following" in self.request.query_params
        username = self.request.query_params.get("username")
        q = self.request.query_params.get("q")
        queryset = self.queryset

        if saved:
            if self.request.user.is_authenticated:
                queryset = queryset.filter(saved_by=self.request.user)
            else:
                queryset = []

        if username:
            queryset = queryset.filter(owner__username=username)

        if following:
            if self.request.user.is_authenticated:
                queryset = queryset.filter(owner__in=self.request.user.following.all())
            else:
                queryset = []

        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(owner__username__icontains=q))

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)




class CommentViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get("post_id")
        queryset = self.queryset

        if post_id:
            queryset = queryset.filter(post=post_id)

        return queryset


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin):
    """Manage recipes in the database"""
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

    def delete(self, request):
        # not found in documentation(as far as I searched)
        # Checking User and Token Table. It is one-to-one relationship.
        request.user.auth_token.delete()  # simply delete the token to force a login
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        # dynamically change the permission classes according to the request METHOD.

        # To delete token , token must be provided in DELETE request.
        if self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class UserRegisterAPIView(generics.GenericAPIView):
    # POST api/auth/register
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        print('Request Data', request.data)
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


class PostSaveActionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [rest_framework.renderers.JSONRenderer]

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)

        if post in request.user.saved_posts.all():
            request.user.saved_posts.remove(post)
            return Response({"result": None, "status_code": status.HTTP_200_OK, "message": "unsaved"}, status=status.HTTP_200_OK)
        else:
            request.user.saved_posts.add(post)
            return Response({"result": None, "status_code": status.HTTP_200_OK, "message": "saved"}, status=status.HTTP_200_OK)


class PostLikeActionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [rest_framework.renderers.JSONRenderer]



    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)

        if post in request.user.liked_posts.all():
            request.user.liked_posts.remove(post)
            return Response({"result": None, "status_code": status.HTTP_200_OK, "message": "unliked"}, status=status.HTTP_200_OK)
        else:
            request.user.liked_posts.add(post)
            return Response({"result": None, "status-code": status.HTTP_200_OK, "message": "liked"}, status=status.HTTP_200_OK)


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [rest_framework.renderers.JSONRenderer]

    def post(self, request, *args, **kwargs):
        current_user = request.user
        pk = kwargs['pk']
        profile_user = get_object_or_404(User, pk=pk)

        if current_user in profile_user.followers.all():
            profile_user.followers.remove(current_user)
            return Response({"result": None, "status_code": status.HTTP_200_OK, "message": "unfollowed"},
                            status=status.HTTP_200_OK)
        else:
            profile_user.followers.add(current_user)
            return Response({"result": None, "status-code": status.HTTP_200_OK, "message": "followed"},
                            status=status.HTTP_200_OK)


