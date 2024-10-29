from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Course, Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "course",
            "student",
            "overall_grade",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "student", "course"]


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    enrollments = EnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "teacher",
            "students",
            "subject",
            "created_at",
            "updated_at",
            "created_by",
            "enrollments",
        ]
