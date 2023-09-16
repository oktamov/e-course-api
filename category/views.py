from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course

from .filters import CategoryFilter
from .models import Category
from .serializers import CategoryListSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.order_by("position")
    serializer_class = CategoryListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter  # noqa

    def filter_queryset(self, queryset):
        parent = self.request.query_params.get("parent")
        if not parent:
            queryset = queryset.filter(parent__isnull=True)
        return super().filter_queryset(queryset)


class CategoryDetailView(APIView):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({"status": 404, "error": "Category not found"})

        courses = Course.objects.filter(category=category)
        course_data = []

        for course in courses:
            course_data.append(
                {"name": course.name, "desc": course.desc, "level": course.get_level_display(), "price": course.price}
            )

        response_data = {"category_name": category.name, "desc": category.description, "courses": course_data}

        return Response(response_data)
