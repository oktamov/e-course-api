from django.urls import reverse
from rest_framework import serializers

from common.models import AboutUs, AboutUsFull


class AboutUsFullInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsFull
        fields = ('name', 'text', 'photo')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context["request"]
        if instance.photo:
            data["photo"] = request.build_absolute_uri(instance.photo)
        return data


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ["title", "description", "image"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context["request"]
        page = request.query_params.get('page')
        if page != "home":
            data["details"] = AboutUsFullInfoSerializer(
                instance.details.order_by("-photo"), many=True, context={"request": request}
            ).data
        else:
            data["detail"] = request.build_absolute_uri(reverse("common:about-us"))
        return data
