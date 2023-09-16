from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from common.models import Category


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
