from datetime import timedelta

import cv2
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _

from category.models import Category
from common.models import BaseModel
from users.models import User
from .utils import validate_video


class Course(BaseModel):
    class CourseLevels(models.TextChoices):
        BEGINNER = "beginner", _("Beginner")
        INTERMEDIATE = "intermediate", _("Intermediate")
        ADVANCED = "advanced", _("Advanced")

    name = models.CharField(_("Name"), max_length=250)
    slug = models.SlugField(unique=True)
    desc = RichTextUploadingField(
        _("Description"),
    )
    price = models.PositiveIntegerField(_("Price"))
    discount = models.PositiveIntegerField()
    level = models.CharField(max_length=32, choices=CourseLevels.choices, default=CourseLevels.BEGINNER)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses_authored")
    categories = models.ManyToManyField(Category, related_name="courses")
    image = models.ImageField(upload_to="course_picture/", blank=True, null=True)
    video = models.FileField(upload_to="course_video/", blank=True, null=True)

    def __str__(self):
        return self.name


class CourseContent(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to="videos/", validators=[validate_video])
    is_public = models.BooleanField(default=False)
    time = models.TimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="contents")
    position = models.IntegerField()

    def __str__(self):
        return self.title

    @property
    def time(self):  # noqa
        video = cv2.VideoCapture(self.video.path)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)
        if frames == 0 or fps == 0:
            return None
        return timedelta(seconds=round(frames / fps))


class ApplyStatus(models.Choices):
    UNPAID = _("Unpaid")
    PAID = _("Paid")


class Rate(models.Choices):
    CHOICE_ONE = 1
    CHOICE_TWO = 2
    CHOICE_THREE = 3
    CHOICE_FOUR = 4
    CHOICE_FIVE = 5


class CourseApply(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="applies")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="applies")
    status = models.CharField(max_length=20, choices=ApplyStatus.choices)

    def __str__(self):
        return str(self.user)


class Review(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rate = models.IntegerField(choices=Rate.choices)
    comment = models.CharField(max_length=400)

    def __str__(self):
        return str(self.user.first_name)


class CourseProgress(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="course_progress")
    course_content = models.ForeignKey("course.CourseContent", on_delete=models.CASCADE, related_name="progress")
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "course_content"]
