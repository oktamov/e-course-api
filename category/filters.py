from django_filters import rest_framework as filters

from category.models import Category


class CategoryFilter(filters.FilterSet):
    parent = filters.CharFilter(field_name="parent__slug")

    class Meta:
        model = Category
        fields = ("parent",)
