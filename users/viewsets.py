from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, RegisterSerializer
from .models import User
from .permissions import IsAdmin
from drf_spectacular.utils import extend_schema  # Import extend_schema decorator


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    http_method_names = ['get', 'post', 'patch', 'delete']

    @extend_schema(
        description="Create a new user. Only admins can create users.",
        request=RegisterSerializer,
        responses={201: RegisterSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
