from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import SubjectSerializer
from .models import Subject


class SubjectViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing subject instances.
    """

    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
