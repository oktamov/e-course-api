from django.db import models

from category.models import Category
from common.models.base import BaseModel


class ApplicationForm(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="application")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ApplicationForm"
