from django.conf import settings
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import Category
from common.models import ApplicationForm
from common.serializers.application_form import ApplicationFormSerializer


class ApplicationFormView(APIView):
    queryset = ApplicationForm.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ApplicationFormSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ApplicationFormSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get("name")
        email = serializer.validated_data.get("email")
        category_id = serializer.validated_data.get("category_id")
        try:
            self.queryset.get_or_create(name=name, email=email, category_id=category_id)
            category = Category.objects.get(pk=category_id)  # noqa
        except Exception:  # noqa
            return Response({"status": "Not Found"})
        message_html = f"course price: \n" f"Level:\n" f"Description: \n"
        subject = f"Course Information CodeKaplan"
        send_mail(
            subject, message_html, from_email=settings.EMAIL_HOST_USER, recipient_list=[email], fail_silently=False
        )
        serializer.save()
        return Response({"detail": "Information about the course has been sent by email "})
