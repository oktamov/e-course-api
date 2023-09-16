from rest_framework import serializers

from common.models.testimonial import Testimonial
from users.models import User


class TestimonialAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "job", "profile_picture")


class TestimonialsSerializer(serializers.ModelSerializer):
    user = TestimonialAuthorSerializer()

    class Meta:
        model = Testimonial
        fields = ("user", "content", "rate")
