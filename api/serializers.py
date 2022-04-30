from rest_framework import serializers
from post.models import Post
from drf_extra_fields.fields import Base64ImageField


class AuthorInfoSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    posted_by = AuthorInfoSerializer(source='author', read_only=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'posted_by', 'title', 'content', 'created_date', 'image']

    def create(self, validated_data):  # override the create method
        request = self.context.get('request')
        validated_data['author'] = request.user  # assign the author to current user
        obj = super().create(validated_data)
        return obj


