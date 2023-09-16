from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from common.models import BaseModel


class ContactUs(models.Model):
    description = RichTextUploadingField()
    country = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    street = models.CharField(max_length=255)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = "ContactUs"

    @property
    def address(self):
        return f"{self.street}, {self.city}, {self.country}"

    @property
    def location(self):
        return {
            "lat": self.lat,
            "lng": self.lng,
        }


class ContactForm(BaseModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ContactForm"
