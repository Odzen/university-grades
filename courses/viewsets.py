from rest_framework import viewsets, status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response

from .serializers import CourseSerializer, EnrollmentSerializer
from users.serializers import UserSerializer
from .models import Course, Enrollment
from users.permissions import IsAdminOrTeacher
from rest_framework.permissions import IsAuthenticated
from users.models import User

@extend_schema_view(
    list=extend_schema(
        description="Returns a list of all the existing paginated Courses with optional filters."
    ),
    retrieve=extend_schema(
        description="Returns a single Course selected by `id`."
    ),
    create=extend_schema(
        description="Create a new Course. Teachers/Admins can create Courses."
    ),
    partial_update=extend_schema(
        description="Updates an existing Course by `id`."
    ),
    destroy=extend_schema(
        description="Deletes an existing Course by `id`."
    ),
    enrollments=extend_schema(
        description="Manage enrollments for a Course. Use POST to enroll a student and GET to list all enrollments for a Course."
    ),
    manage_enrollment=extend_schema(
        description="Manage a single enrollment for a Course. Use PATCH to update an enrollment and DELETE to remove an enrollment."
    ),
    assignments=extend_schema(
        description="Manage the teacher assigned to a Course. Use POST to assign a teacher, DELETE to remove the teacher and GET to list the teacher assigned to a Course."
    )
)
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    http_method_names = ['get', 'patch', 'delete', 'post']

    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'teacher', 'created_by']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at', 'start_date', 'end_date']
    ordering = ['name']

    def get_queryset(self):
        # Allow admins to see all courses
        if self.request.user.role == "ADMIN":
            return Course.objects.all()

        return Course.objects.filter(teacher=self.request.user)

    def perform_update(self, serializer):
        if (self.request.user.role == "USER" and self.request.user.type == "TEACHER") or self.request.user.role == "ADMIN":
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this course.")

    def perform_destroy(self, instance):
        if self.request.user.role == "ADMIN":
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this course.")

    @action(detail=True, methods=['GET', 'POST'])
    def enrollments(self, request, pk):

        course = self.get_object()

        if request.method == "POST":
            student_id = request.data.get('student', None)

            if student_id is None:
                return Response({"error": "The student field is required."}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(student_id, int) or student_id <= 0:
                return Response({"error": "Student ID must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=student_id)
            except User.DoesNotExist:
                return Response({"error": "The specified student does not exist."}, status=status.HTTP_404_NOT_FOUND)

            if user.role != "USER" or user.type != "STUDENT":
                return Response({"error": "The specified user is not a student."}, status=status.HTTP_400_BAD_REQUEST)

            prerequisites = course.subject.prerequisites.all()
            passed_courses = Enrollment.objects.filter(student=user, overall_grade__gte=3)

            if prerequisites.exists():
                if not all(prereq.id in passed_courses.values_list('course_id', flat=True) for prereq in prerequisites):
                    return Response(
                        {"error": "The student has not completed the prerequisite courses with a passing grade."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = EnrollmentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(course=course, student=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "GET":
            enrollments = Enrollment.objects.filter(course=course)
            serializer = EnrollmentSerializer(enrollments, many=True)
            return Response(serializer.data)

    @action(detail=True, methods=['PATCH', 'DELETE'], url_path='enrollments/(?P<student_id>[^/.]+)')
    def manage_enrollment(self, request, pk, student_id):
        course = self.get_object()

        try:
            enrollment = Enrollment.objects.get(student_id=student_id, course=course)
        except Enrollment.DoesNotExist:
            return Response({"error": "The specified enrollment does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = EnrollmentSerializer(enrollment, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        if request.method == "DELETE":
            enrollment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET', 'POST', 'DELETE'])
    def assignments(self, request, pk):
        course = self.get_object()

        if request.method == "POST":
            teacher_id = request.data.get('teacher')

            if not isinstance(teacher_id, int) or teacher_id <= 0:
                return Response(
                    {"error": "Teacher ID must be a positive integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                teacher_user = User.objects.get(id=teacher_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "The specified teacher user does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if teacher_user.role != "USER" or teacher_user.type != "TEACHER":
                return Response(
                    {"error": "The specified user is not a teacher."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            course.teacher = teacher_user
            course.save()
            return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            course.teacher = None
            course.save()
            return Response(CourseSerializer(course).data, status=status.HTTP_204_NO_CONTENT)

        if request.method == "GET":
            teacher = course.teacher

            if not teacher:
                return Response({"error": "This course does not have a teacher assigned."}, status=status.HTTP_404_NOT_FOUND)

            return Response(UserSerializer(teacher).data)


