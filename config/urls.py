from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title="e-course.uz OPEN API",
        default_version="v1",
        description="Online Education Platform API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ecourse.uz@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", include("common.urls"), name="common"),
    path("courses/", include("course.urls"), name="courses"),
    path("categories/", include("category.urls"), name="category"),
    path("bot/", include("bot.urls"), name="bot"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('payments/', include('checkout.urls')),
    path('cards/', include('card.urls')),

]

swagger_urls = [
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += swagger_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
