from rest_framework import serializers

from common.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context["request"]
        parent = request.query_params.get("parent")
        if parent:
            data["children"] = CategorySerializer(instance.children, many=True).data
        return data
