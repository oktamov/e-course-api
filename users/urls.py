from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.social_login.views import FacebookSocialAuthView, GoogleSocialAuthView
from users.views import (
    CheckEmailVerificationCodeView,
    CheckEmailVerificationCodeWithParams,
    CustomTokenObtainPairView,
    ProfileView,
    RegisterAPIView,
    SendEmailVerificationCodeView,
    SendPhoneVerificationCodeView,
    UserApplyCoursesView
)

urlpatterns = [
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/facebook/", FacebookSocialAuthView.as_view(), name="facebook_login"),
    path("auth/google/", GoogleSocialAuthView.as_view(), name="google_login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("courses/", UserApplyCoursesView.as_view(), name="user_apply_courses"),
    path("email/verification/", SendEmailVerificationCodeView.as_view(), name="send-email-code"),
    path("email/check-verification/", CheckEmailVerificationCodeView.as_view(), name="check-email-code"),
    path("email/check-verification-code/", CheckEmailVerificationCodeWithParams.as_view(), name="check-email"),
    path("phone/verification-code/", SendPhoneVerificationCodeView.as_view()),
]
