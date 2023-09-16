from django.conf import settings
from django.urls import path

from course.views import (
    CourseApplyView,
    CourseContentListView,
    CourseDetailView,
    CourseExportView,
    CourseImportView,
    CourseListView,
    CourseReviewDetailView,
    CourseReviewListView, CourseContentDetailView,
)

urlpatterns = [
    path("", CourseListView.as_view(), name="course-api"),
    path("<slug:slug>/", CourseDetailView.as_view(), name="course-detail"),
    path("<slug:slug>/contents/", CourseContentListView.as_view(), name="course-content"),
    path("<slug:slug>/contents/<int:content_id>/", CourseContentDetailView.as_view(), name="course-content"),
    path("<slug:slug>/reviews/", CourseReviewListView.as_view(), name="course-review-list"),
    path("reviews/<int:pk>/", CourseReviewDetailView.as_view(), name="course-review-detail"),
    path("<slug:slug>/apply/", CourseApplyView.as_view(), name="apply-course"),
]
import_export_urlpatterns = [
    path("export/", CourseExportView.as_view(), name="export"),
    path("import/", CourseImportView.as_view(), name="import"),
]
if settings.DEBUG is False:
    urlpatterns += import_export_urlpatterns
