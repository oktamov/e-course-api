from django.db import models

from common.models import BaseModel


class Rate(models.Choices):
    CHOICE_ONE = 1
    CHOICE_TWO = 2
    CHOICE_THREE = 3
    CHOICE_FOUR = 4
    CHOICE_FIVE = 5


class Testimonial(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="testimonials")
    content = models.TextField()
    rate = models.IntegerField(choices=Rate.choices)

    def __str__(self):
        return str(self.user.full_name)
