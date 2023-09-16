from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="about/images/")
    video_file = models.FileField(upload_to="about/videos/", blank=True, null=True)
    video_poster = models.ImageField(upload_to="about/images/", blank=True, null=True)
    details = models.ManyToManyField('AboutUsFull', related_name='details')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "AboutUs"


class AboutUsFull(models.Model):
    name = models.CharField(max_length=255)
    text = RichTextUploadingField()
    photo = models.ImageField(upload_to="about/images/", null=True, blank=True)

    def __str__(self):
        return self.name
