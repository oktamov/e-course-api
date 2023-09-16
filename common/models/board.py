from django.db import models

from common.models import BaseModel


class Board(BaseModel):
    title = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title[:50]


class BoardLogoTitle(models.Model):
    board = models.ForeignKey(Board, models.CASCADE, related_name='boards')
    title = models.CharField(max_length=128)
    logo = models.ImageField()
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.board.title} - {self.title}"
