from django_filters import rest_framework as filters

from course.models import Course


class ListFilter(filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = "in"
        values = value.split(",")
        return super(ListFilter, self).filter(qs, values)


class CourseFilter(filters.FilterSet):
    section = ListFilter(field_name="categories__parent__parent__slug", lookup_expr="in")
    sub_categories = ListFilter(field_name="categories__slug", lookup_expr="in")

    class Meta:
        model = Course
        fields = ("section", "sub_categories")
