from rest_framework import serializers
from post.models import Post
from drf_extra_fields.fields import Base64ImageField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    posted_by = UserInfoSerializer(source='author', read_only=True)
    image = Base64ImageField(allow_null=True)
    # is_liked = serializers.BooleanField(default=False)
    # is_saved = serializers.BooleanField(default=False)


    class Meta:
        model = Post
        fields = ['id', 'posted_by', 'title', 'content', 'created_date', 'image', 'like_counts']

    def create(self, validated_data):  # override the create method
        print(validated_data)
        request = self.context.get('request')

        validated_data['author'] = request.user  # assign the author to the current user
        print(validated_data)
        obj = super().create(validated_data)
        return obj

    # def to_internal_value(self, data):
    #     request = self.context.get('request')
    #     data['title'] = "hello"
    #     data['test'] = "test"
    #     print(data)
    #
    #     return super().to_internal_value(data)

    def to_representation(self, instance):
        request = self.context.get('request')
        user = request.user
        representation = super().to_representation(instance)
        representation['is_liked'] = False
        representation['is_saved'] = False
        representation['is_owner'] = False
        print(user)
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
        # required=False
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
        attrs['user'] = user
        # print(attrs)
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # https://www.django-rest-framework.org/api-guide/serializers/#additional-keyword-arguments
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
