from rest_framework import serializers

from category.serializers import CategorySerializer
from course.models import Course, CourseContent, Review
from users.models import User


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "slug", "image", "name", "desc", "level", "price")


class CourseSerializerForLog(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = ("id", "title", "description", "video", "is_public", "time", "course", "position")
        read_only_fields = ("id",)


class CourseAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "profile_picture", "job")


class CourseDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    categories = CategorySerializer(many=True)
    author = CourseAuthorSerializer()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "slug",
            "author",
            "image",
            "video",
            "desc",
            "price",
            "discount",
            "level",
            "categories",
        )


class CourseReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "user", "course", "rate", "comment")


class ImportFileSerializer(serializers.Serializer):
    file = serializers.FileField()
