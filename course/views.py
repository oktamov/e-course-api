from datetime import datetime
from io import BytesIO

import pandas as pd
from django.db.models import Count
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course, Review, CourseProgress, CourseContent
from course.serializers import (
    CourseContentSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    CourseReviewSerializer,
    ImportFileSerializer, )
from pagination import CustomPagination
from permissions import IsReviewAuthor
from .exceptions import ContentNotCompleted
from .filters import CourseFilter
from .models import CourseApply
from .openapi_params import is_popular_param


@method_decorator(name="get", decorator=swagger_auto_schema(manual_parameters=[is_popular_param]))
class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CourseFilter  # noqa
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Course.objects.order_by("-id")
        query_params = self.request.query_params
        is_popular = query_params.get("is_popular")
        if is_popular == "true":
            queryset = queryset.annotate(applies_count=Count("applies")).order_by("-applies_count")
        return queryset


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = "slug"


class CourseContentListView(APIView):
    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=kwargs.get("slug"))
        serializer = CourseContentSerializer(course.contents.order_by("position"), many=True)
        return Response(serializer.data)


class CourseReviewListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        reviews = Review.objects.filter(course_id=self.kwargs.get("pk"))
        serializer = CourseReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseReviewSerializer)
    def post(self, request):
        serializer = CourseReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)


class CourseReviewDetailView(APIView):
    permission_classes = [IsAuthenticated, IsReviewAuthor]

    def get(self, request, *args, **kwargs):
        course_content = get_object_or_404(Review, id=kwargs.get("pk"))
        serializer = CourseReviewSerializer(course_content)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseReviewSerializer)
    def put(self, request, *args, **kwargs):
        queryset = get_object_or_404(Review, id=kwargs.get("pk"))
        self.check_object_permissions(request, queryset)
        serializer = CourseReviewSerializer(instance=queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)


class CourseApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course = get_object_or_404(Course, slug=kwargs.get("slug"))
        if CourseApply.objects.filter(course=course, user=user).exists():
            return Response({"error": _("You have already applied for the course.")})
        CourseApply.objects.create(user=user, course=course)
        return Response({"status": _("Your application has been accepted.")})


class CourseExportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        columns = {
            "id": "ID",
            "name": "Nomi",
            "desc": "Batafsil ma'lumot",
            "level": "Daraja",
            "price": "Narxi",
            "author__first_name": "author__first_name",
            "author__last_name": "author__last_name",
        }
        df = pd.DataFrame(
            list(
                Course.objects.values("id", "name", "desc", "level", "price", "author__first_name", "author__last_name")
            ),
            columns=list(columns.keys()),
        )
        df["full_name"] = df["author__first_name"] + " " + df["author__last_name"]
        df.drop(columns=["author__first_name", "author__last_name"], inplace=True)
        columns.update({"full_name": "Muallif"})
        df.rename(columns=columns, inplace=True)

        file_like_object = BytesIO()
        df.to_excel(file_like_object, index=False)
        file_like_object.seek(0)  # move to the beginning of file
        response = FileResponse(file_like_object)
        filename = f"Courses_{datetime.now().strftime('%Y%m%d_%H%M')}"
        response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'

        return response


class CourseImportView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body=ImportFileSerializer)
    def post(self, request):
        serializer = ImportFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = request.FILES.get("file")
        df = pd.read_excel(file)
        for index, row in df.iterrows():
            Course.objects.update_or_create(
                id=row["ID"],
                defaults={
                    "name": row["Nomi"],
                    "desc": row["Batafsil ma'lumot"],
                    "price": row["Narxi"],
                    "level": row["Daraja"],
                },
            )
        return Response("Course import started.")


class CourseContentDetailView(APIView):

    def get(self, request, *args, **kwargs):
        content_id = kwargs.get("content_id")
        content = get_object_or_404(CourseContent, id=content_id)
        user = request.user
        if user.is_authenticated:
            if content.course.applies.filter(user=user).exists():
                all_content_ids = list(content.course.contents.order_by("position").values_list("id", flat=True))
                index = all_content_ids.index(content_id)
                prev2_content_id = content_id if index == 0 else all_content_ids[index - 2]
                prev2_content = CourseContent.objects.filter(id=prev2_content_id).first()
                content_progress = CourseProgress.objects.filter(user=user, course_content=prev2_content).first()
                if content_progress and content_progress.is_completed:
                    raise ContentNotCompleted
                previous_content_id = content_id if index == 0 else all_content_ids[index - 1]
                previous_content = CourseContent.objects.filter(id=previous_content_id).first()
                if previous_content:
                    previous_progress, _ = CourseProgress.objects.update_or_create(
                        user=user, course_content=previous_content, defaults={"is_completed": True}
                    )
                next_progress, _ = CourseProgress.objects.get_or_create(user=user, course_content=content)
        serializer = CourseContentSerializer(content)
        return Response(serializer.data)
