from rest_framework import serializers
from .models import Subject
from courses.serializers import CourseSerializer


class SubjectSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    created_by = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    prerequisites = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ["id", "name","number_credits","semester", "level", "program", "created_at", "updated_at", "created_by", "prerequisites", "courses"]
