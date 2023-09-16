from django.db import models
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True)
    position = models.PositiveSmallIntegerField(default=1)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.name.upper():
            self.slug = slugify(self.name.lower())
        self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name_plural = "Category"
