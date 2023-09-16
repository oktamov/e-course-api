from rest_framework import generics

from common.models import Blog
from common.serializers.blog_serializers import BlogSerializer
from pagination import CustomPagination


class BlogList(generics.ListAPIView):
    queryset = Blog.objects.order_by("-created_at")
    serializer_class = BlogSerializer
    pagination_class = CustomPagination


class BlogDetail(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.views_count = blog.views_count + 1
        blog.save(update_fields=["views_count"])
        return super().retrieve(request, *args, **kwargs)
