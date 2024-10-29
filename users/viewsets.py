from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Enrollment
from courses.serializers import EnrollmentSerializer
from .models import User
from .permissions import IsAdminOrTeacherForStudents
from .serializers import UserSerializer, RegisterSerializer


@extend_schema_view(
    list=extend_schema(
        description="Returns a list of all the existing paginated Users with optional filters."
    ),
    retrieve=extend_schema(description="Returns a single User selected by `id`."),
    create=extend_schema(
        description="Create a new User. Only Admins can create Users.",
        request=RegisterSerializer,
        responses={201: RegisterSerializer},
    ),
    partial_update=extend_schema(description="Updates an existing User by `id`."),
    destroy=extend_schema(description="Deletes an existing User by `id`."),
    enrollments=extend_schema(
        description="Manage enrollments for a Student, use GET to retrieve the courses that the Student is enrolled in."
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrTeacherForStudents]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["type", "role", "created_by"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = ["first_name", "last_name", "created_at", "updated_at"]

    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action == "list_student_enrollments":
            permission_classes = [IsAuthenticated]
        elif self.request.method in ["GET", "POST", "PATCH", "DELETE"]:
            permission_classes = [IsAuthenticated, IsAdminOrTeacherForStudents]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = User.objects.all()

        if self.request.user.role == "USER" and self.request.user.type == "TEACHER":
            queryset = queryset.filter(type="STUDENT")

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["get"],
        url_path="students/(?P<student_id>[^/.]+)/enrollments",
    )
    def list_student_enrollments(self, request, student_id=None):
        try:
            student = User.objects.get(pk=student_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND
            )

        enrollments = Enrollment.objects.filter(student=student)

        if request.user.type == "STUDENT":

            if request.user.pk != student.pk:
                return Response(
                    {"error": "Students can only view their own enrollments."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        elif request.user.type == "TEACHER" and request.user.role == "USER":
            enrollments = Enrollment.objects.filter(
                student=student, course__teacher=request.user
            )

        approved = request.query_params.get("approved")
        overall = request.query_params.get("overall")

        if approved is not None:
            if approved.lower() == "true":
                enrollments = enrollments.filter(overall_grade__gte=3)
            else:
                enrollments = enrollments.filter(overall_grade__lt=3)

        if overall and overall.lower() == "true":
            average_score = enrollments.aggregate(Avg("overall_grade"))[
                "overall_grade__avg"
            ]
            return Response(
                {
                    "enrollments": EnrollmentSerializer(enrollments, many=True).data,
                    "overall_average_score": average_score,
                }
            )

        return Response(EnrollmentSerializer(enrollments, many=True).data)
