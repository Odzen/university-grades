from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.filters import CourseFilter
from courses.serializers import CourseSerializer
from users.permissions import IsAdmin
from .models import Subject
from .serializers import SubjectSerializer


@extend_schema_view(
    list=extend_schema(
        description="Returns a list of all the existing paginated Subjects with optional filters."
    ),
    retrieve=extend_schema(description="Returns a single Subject selected by `id`."),
    create=extend_schema(
        description="Create a new Subject. Only Admins can create Subjects."
    ),
    partial_update=extend_schema(description="Updates an existing Subject by `id`."),
    destroy=extend_schema(description="Deletes an existing Subject by `id`."),
    courses=extend_schema(
        description="Manage courses for a Subject. Use POST to add a course and GET to list all courses."
    ),
    prerequisites=extend_schema(
        description="Manage prerequisites for a Subject. Use POST to add a prerequisite, DELETE to remove one and GET to list all prerequisites.",
    ),
)
class SubjectViewSet(viewsets.ModelViewSet):

    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    http_method_names = ["get", "post", "patch", "delete"]

    permission_classes = [IsAuthenticated, IsAdmin]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["level", "semester", "created_by", "number_credits"]
    search_fields = ["name", "program"]
    ordering = ["name", "number_credits", "semester", "created_at", "updated_at"]

    def create(self, request, *args, **kwargs):
        serializer = SubjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["GET", "POST", "DELETE"])
    def prerequisites(self, request, pk):
        subject = self.get_object()

        if request.method == "POST":
            prerequisite_id = request.data.get("prerequisite")

            if not isinstance(prerequisite_id, int) or prerequisite_id <= 0:
                return Response(
                    {"error": "Prerequisite ID must be a positive integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                prerequisite_subject = Subject.objects.get(id=prerequisite_id)
            except Subject.DoesNotExist:
                return Response(
                    {"error": "The specified prerequisite subject does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if subject.id == prerequisite_subject.id:
                return Response(
                    {"error": "A subject cannot be a prerequisite of itself."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subject.prerequisites.add(prerequisite_subject)
            subject.save()
            return Response(
                SubjectSerializer(subject).data, status=status.HTTP_201_CREATED
            )

        if request.method == "DELETE":
            prerequisite_id = request.data.get("prerequisite")

            if not isinstance(prerequisite_id, int) or prerequisite_id <= 0:
                return Response(
                    {"error": "Prerequisite ID must be a positive integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                prerequisite_subject = Subject.objects.get(id=prerequisite_id)
            except Subject.DoesNotExist:
                return Response(
                    {"error": "The specified prerequisite subject does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not subject.prerequisites.filter(id=prerequisite_id).exists():
                return Response(
                    {
                        "error": "The specified prerequisite is not associated with this subject."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subject.prerequisites.remove(prerequisite_subject)
            subject.save()
            return Response(
                SubjectSerializer(subject).data, status=status.HTTP_204_NO_CONTENT
            )

        if request.method == "GET":
            prerequisites = subject.prerequisites.all()
            return Response(SubjectSerializer(prerequisites, many=True).data)

    @action(detail=True, methods=["GET", "POST"], serializer_class=CourseSerializer)
    def courses(self, request, pk):
        subject = self.get_object()
        data = request.data.copy()
        data["subject"] = subject.id
        data["created_by"] = request.user.id

        if request.method == "POST":
            serializer = CourseSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "GET":
            courses = subject.courses.all()

            filtered_courses = CourseFilter(request.GET, queryset=courses).qs

            page = self.paginate_queryset(filtered_courses)
            if page is not None:
                serializer = CourseSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = CourseSerializer(filtered_courses, many=True)
            return Response(serializer.data)
