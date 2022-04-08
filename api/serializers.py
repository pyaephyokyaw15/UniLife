from rest_framework import serializers
from post.models import Post


class OwnerInfoSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    posted_by = OwnerInfoSerializer(source='owner', read_only=True)

    class Meta:
        model = Post
        fields = ['posted_by', 'title', 'content', 'date_posted']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        obj = super().create(validated_data)
        return obj


