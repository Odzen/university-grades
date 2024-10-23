from .serializers import SubjectSerializer
from .models import Subject
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)


class ListUsersView(ListAPIView, CreateAPIView):
    """
    Get all users or create a new user
    """

    allowed_methods = ["GET", "POST"]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class DetailUserView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ["GET", "PUT", "DELETE"]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
