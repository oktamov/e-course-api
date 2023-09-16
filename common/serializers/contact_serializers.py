from rest_framework import serializers

from common.models import ContactForm, ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["description", "address", "email", "phone", "location"]


class ContactFormListSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ContactForm
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "message",
        ]
