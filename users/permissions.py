from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "TEACHER"


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "STUDENT"


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"
