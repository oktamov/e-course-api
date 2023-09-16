from rest_framework import serializers

from common.models import ApplicationForm


class ApplicationFormSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        model = ApplicationForm
        fields = (
            "id",
            "name",
            "email",
            "category_id",
        )
        read_only_fields = ("id",)
