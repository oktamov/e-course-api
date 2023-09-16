import pytest
from django.urls import reverse
from django_filters.compat import TestCase
from rest_framework import status

from common.serializers import BlogSerializer


@pytest.mark.django_db
class BlogtListViewTest(TestCase):
    url = reverse("common:blog-list")
    blog_data = {
        "title": "Test Blog",
        "slug": "test",
        "description": "Test BlogList",
        "author": "John Doe",
        "views_count": 123456789,
    }

    def setUp(self):
        self.serializer = BlogSerializer(data=self.blog_data)

    def test_list_blog(self):
        response = self.client.post(self.url, self.blog_data)
