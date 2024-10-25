from rest_framework import permissions


class IsAdminOrTeacherForStudents(permissions.BasePermission):
    """
    Custom permission to only allow Admins to manage all users,
    and Teachers to manage only Students.
    """

    def has_permission(self, request, view):
        if request.user.role == "ADMIN":
            return True

        if request.user.role == "USER" and request.user.type == 'TEACHER':
            if view.action in ['list', 'retrieve']:
                return True

            if view.action in ['create', 'update', 'partial_update', 'destroy']:
                return request.data['role'] == 'USER' and request.data[
                    'type'] == 'STUDENT' if 'type' in request.data else True

        return False


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "TEACHER"


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "STUDENT"


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"


class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN" or (request.user.role == "USER" and request.user.type == "TEACHER")
