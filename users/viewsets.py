from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import (
    UserSerializer, RegisterSerializer
)
from .models import User
from .permissions import IsAdminOrTeacherForStudents



@extend_schema_view(
    list=extend_schema(
        description="Returns a list of all the existing paginated Users with optional filters."
    ),
    retrieve=extend_schema(
        description="Returns a single User selected by `id`."
    ),
    create=extend_schema(
        description="Create a new User. Only Admins can create Users.",
        request=RegisterSerializer,
        responses={201: RegisterSerializer},
    ),
    partial_update=extend_schema(
        description="Updates an existing User by `id`."
    ),
    destroy=extend_schema(
        description="Deletes an existing User by `id`."
    )
)
class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IsAdminOrTeacherForStudents]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'role', 'created_by']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name', 'created_at', 'updated_at']

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = User.objects.all()

        if self.request.user.role == "USER" and self.request.user.type == 'TEACHER':
            queryset = queryset.filter(type='STUDENT')

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)