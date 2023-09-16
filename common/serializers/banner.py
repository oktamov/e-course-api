from rest_framework import serializers

from common.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("title", "description", "image")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context["request"]
        data["image"] = request.build_absolute_uri(instance.image.url)
        return data
