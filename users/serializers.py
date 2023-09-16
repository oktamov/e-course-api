from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .utils import phone_validator


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "job",
            "address",
            "birth_date",
            "age",
            "type",
        )


class CustomTokenObtainPairSerializer(serializers.Serializer):
    token_class = RefreshToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"] = serializers.CharField()
        self.fields["password"] = PasswordField()

    default_error_messages = {"no_active_account": _("No active account found with the given credentials")}

    def validate(self, attrs):
        data = super().validate(attrs)
        username_or_email = data.pop("username", None)
        user = authenticate(
            request=self.context.get("request"),
            email=username_or_email,
            username=username_or_email,
            password=data.pop("password", None),
        )

        if not api_settings.USER_AUTHENTICATION_RULE(user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        data["user"] = UserInfoSerializer(user).data
        data["tokens"] = user.tokens

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "job",
            "address",
            "birth_date",
            "age",
            "profile_picture",
        )
        read_only_fields = ("id",)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        username = validated_data.pop("username", None)
        try:
            validate_email(username)
        except ValidationError:
            validated_data["username"] = username
            validated_data["email"] = None
        else:
            validated_data["email"] = username
            validated_data["username"] = None
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SendEmailVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SendPhoneVerificationCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, validators=[phone_validator])


class CheckEmailVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
