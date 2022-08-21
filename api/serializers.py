from rest_framework import serializers
from post.models import Post, Comment
from drf_extra_fields.fields import Base64ImageField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from django.conf import settings
from accounts.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'university', 'profile_picture']
        read_only_fields = ['id', 'username']  # show only on GET request

    def update(self, instance, validated_data):  # override update method
        print(validated_data)

        # get the current(before update) profile_picture
        profile_picture = instance.profile_picture
        print("profile_picture", profile_picture)

        # update user with the validated data(front-end sent data)
        user = super().update(instance, validated_data)

        if not user.profile_picture:
            # frontend send null if the image is not changed.
            # If image is null, set image the current(before update) image.
            user.profile_picture = profile_picture
            user.save()
        return user

    def to_representation(self, instance):  # override the serializer response
        representation = super().to_representation(instance)

        # this serializer is also used in data return.
        # In this case, request context does not exist.
        try:
            request = self.context.get('request')

            # check the current viewing profile is the current user's profile or not
            # 'self_profile' attribute is added to help the frontend developer know whether profile can be edited or not
            if request.method == "GET":
                user = request.user
                if instance == user:
                    representation['is_self_profile'] = True
                else:
                    representation['is_self_profile'] = False

                if user in request.user.following.all():
                    representation['is_following'] = True

                else:
                    representation['is_following'] = False



        except:
            None
        return representation


class CommentSerializer(serializers.ModelSerializer):
    owner = UserInfoSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='api:comment-detail', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'owner', 'created_date', 'post', 'url']

        # override the error message
        extra_kwargs = {
            "comment": {"error_messages": {"required": "comment is required"}},
            "post": {"error_messages": {"required": "post is required"}},
        }

    def create(self, validated_data):  # override the create method
        print(validated_data)
        request = self.context.get('request')

        validated_data['owner'] = request.user  # assign the owner to the current user
        print(validated_data)
        obj = super().create(validated_data)
        return obj

    def to_representation(self, instance):  # override the serializer response
        request = self.context.get('request')
        user = request.user
        representation = super().to_representation(instance)

        # 'is_owner' attribute is added to help the frontend developer know whether comment can be edited or not
        representation['is_owner'] = False
        # print(user)
        if not user.is_anonymous:
            # print(instance)
            if instance in user.comments.all():
                representation['is_owner'] = True
        return representation


class PostSerializer(serializers.ModelSerializer):
    owner = UserInfoSerializer(read_only=True)
    image = Base64ImageField(allow_null=True)
    url = serializers.HyperlinkedIdentityField(view_name='api:post-detail', read_only=True)
    image_removed = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'content', 'created_date', 'image', 'like_counts', 'comment_counts', 'url', 'image_removed']
        # override the error message
        extra_kwargs = {
            "title": {"error_messages": {"required": "Title is required"}},
            "content": {"error_messages": {"required": "Content is required"}},
        }

    def create(self, validated_data):  # override the create method
        print(validated_data)
        request = self.context.get('request')

        validated_data['owner'] = request.user  # assign the owner to the current user
        print(validated_data)
        del validated_data['image_removed']
        obj = super().create(validated_data)
        return obj

    def update(self, instance, validated_data):  # override the update method
        print(validated_data)
        image_removed = validated_data['image_removed']

        # get the current(before update) image
        print("image", instance.image)
        image = instance.image

        # update post with the validated data(front-end sent data)
        del validated_data['image_removed']
        post = super().update(instance, validated_data)

        if image_removed:
            # front-end set image_removed field True if the image is removed.
            post.image = None

        elif not post.image:
            # front-end send null if the image is not changed.
            # If image is null, set image the current image.
            post.image = image
            post.save()

        return post

    def to_representation(self, instance):  # override the serializer response
        request = self.context.get('request')
        user = request.user
        representation = super().to_representation(instance)
        representation['is_liked'] = False
        representation['is_saved'] = False
        representation['is_owner'] = False  # 'help the frontend developer know whether post can be edited or not
        # print(user)

        if not user.is_anonymous:
            print(instance)

            # check liked or not for the current user
            if instance in user.liked_posts.all():
                representation['is_liked'] = True

            if instance in user.saved_posts.all():
                representation['is_saved'] = True

            if instance in user.posts.all():
                representation['is_owner'] = True

        return representation


class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'content', 'created_date', 'image', 'like_counts',
                  'comment_counts', 'comments', 'image_removed']


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Invalid username or password.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        # print('Attrs', attrs)
        attrs['user'] = user  # add user to serializer response
        # print(attrs)
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'university', 'profile_picture']
        # override error message
        extra_kwargs = {
            "username": {"error_messages": {"required": "username is required"}},
            "password": {"error_messages": {"required": "password is required"}},
            "first_name": {"required": True, "error_messages": {"required": "first_name is required"}},
            "last_name": {"required": True, "error_messages": {"required": "last_name is required"}},
            "university": {"required": True, "error_messages": {"required": "university is required"}}
        }

    # https://www.django-rest-framework.org/api-guide/serializers/#additional-keyword-arguments
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_picture=validated_data['profile_picture'],
            university=validated_data['university']
        )
        user.set_password(validated_data['password'])  # hash password
        user.save()
        return user


class UserProfileSerializer(UserInfoSerializer):
    posts = PostDetailSerializer(many=True, read_only=True)
    # following = serializers.PrimaryKeyRelatedField(queryset=User.following, many=True)
    following = UserInfoSerializer(many=True)
    followers = UserInfoSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'university', 'profile_picture', 'posts', 'followers', 'following']
        read_only_fields = ['id', 'username', 'posts']  # show only on GET request
