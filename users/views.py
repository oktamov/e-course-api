from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.urls import reverse
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from course.models import Course
from course.serializers import CourseListSerializer
from users.serializers import (
    CheckEmailVerificationCodeSerializer,
    RegisterSerializer,
    SendEmailVerificationCodeSerializer,
    SendPhoneVerificationCodeSerializer,
    UserInfoSerializer,
)
from .models import User, VerificationCode
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserDetailSerializer,
    UserSerializer,
)
from .tasks import send_verification_code


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        if User.objects.filter(Q(username=username) | Q(email=username)).exists():
            return Response({"error": "Username or email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        data = {"user": UserInfoSerializer(user).data, "tokens": user.tokens}
        return Response(data=data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserDetailSerializer)
    def put(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserApplyCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        course_ids = user.applies.values_list('id', flat=True).order_by('-created_at')
        courses = Course.objects.filter(id__in=course_ids)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)


class SendEmailVerificationCodeView(APIView):
    @swagger_auto_schema(request_body=SendEmailVerificationCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendEmailVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = get_random_string(allowed_chars="0123456789", length=6)
        verification_code, _ = VerificationCode.objects.update_or_create(
            email=email, defaults={"code": code, "is_verified": False}
        )
        verification_code.expired_at = verification_code.last_sent_time + timedelta(seconds=30)
        verification_code.save(update_fields=["expired_at"])
        subject = "Email registration"
        verification_email_url = reverse("check-email")
        message = (
            f"Click to confirm email:\n " f"http://localhost:8000{verification_email_url}?email={email}&code={code}"
        )
        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
        return Response({"detail": "Successfully sent email verification code."})


class CheckEmailVerificationCodeView(CreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = CheckEmailVerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")
        verification_code = (
            self.get_queryset().filter(email=email, is_verified=False).order_by("-last_sent_time").first()
        )
        if verification_code and verification_code.code != code and verification_code.is_expire:
            raise ValidationError("Verification code invalid.")
        verification_code.is_verified = True
        verification_code.save(update_fields=["is_verified"])
        return Response({"detail": "Verification code is verified."})


class CheckEmailVerificationCodeWithParams(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        code = request.query_params.get("code")
        verification_code = (
            VerificationCode.objects.filter(email=email, is_verified=False).order_by("-last_sent_time").first()
        )
        if verification_code and verification_code.code != code:
            raise ValidationError("Verification code invalid.")
        verification_code.is_verified = True
        verification_code.save(update_fields=["is_verified"])
        return Response({"detail": "Verification code is verified."})


class SendPhoneVerificationCodeView(APIView):
    @swagger_auto_schema(request_body=SendPhoneVerificationCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendPhoneVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        code = get_random_string(allowed_chars="0123456789", length=6)
        verification_code, _ = VerificationCode.objects.update_or_create(
            phone=phone, defaults={"code": code, "is_verified": False}
        )
        send_verification_code.delay(phone, code)
        return Response({"detail": "Verification code sent."})
