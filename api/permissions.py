from rest_framework.permissions import BasePermission


class IsTutor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 2

class IsUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'role' attribute set to 'tutor'
        return request.user.is_authenticated and request.user.role == 3

    def has_object_permission(self, request, view, obj):
        # Allow tutors to modify their own objects
        return obj.user == request.user
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 1