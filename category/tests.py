from django.test import Client, TestCase
from django.urls import reverse

from .models import Category


client = Client()


class TestCategory(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(
            name="backend",
            description="test",
            position=1,
        )

    def test_list_category(self):
        url = reverse("common:category-list")
        response = client.get(url)
        self.assertEquals(response.status_code, 200)
