from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin

from category.models import Category
from .models import Course, CourseContent, CourseProgress, CourseApply, Review
from .resources import CourseResource


@admin.register(Course)
class AdminCourse(ImportExportModelAdmin, TabbedTranslationAdmin):
    resource_classes = [CourseResource]
    prepopulated_fields = {"slug": ("name_uz",)}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["queryset"] = Category.objects.filter(level=2)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(CourseContent)
class AdminCourseContent(admin.ModelAdmin):
    list_display = ("id", "title", "description", "video", "time", "is_public", "course", "position")


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "course_content", "is_completed")


admin.site.register(Review)
admin.site.register(CourseApply)
