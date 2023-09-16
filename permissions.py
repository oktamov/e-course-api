from rest_framework.permissions import BasePermission


class IsBlogAuthor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author)


class IsCourseAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return bool(obj.author == request.user)
        return request.method in ["GET", "HEAD", "OPTIONS"]


class IsReviewAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.author == request.user
        return request.method in ["GET", "HEAD", "OPTIONS"]


class IsCardUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.user == request.user
        return request.method in ["GET", "HEAD", "OPTIONS"]
