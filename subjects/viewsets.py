from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import SubjectSerializer
from .models import Subject
from users.permissions import IsAdmin, IsTeacher


class SubjectViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing subject instances.
    """

    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    http_method_names = ['get', 'post', 'patch', 'delete']

    permission_classes = [IsAuthenticated, IsAdmin]
