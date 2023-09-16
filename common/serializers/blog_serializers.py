from rest_framework import serializers

from common.models import Blog
from users.models import User


class BlogAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "profile_picture")


class BlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    author = BlogAuthorSerializer()

    class Meta:
        model = Blog
        fields = ["id", "image", "slug", "title", "description", "author", "views_count", "created_at"]
