from .serializers import UserSerializer
from .models import User
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)


class ListUsersView(ListAPIView, CreateAPIView):
    allowed_methods = ["GET", "POST"]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class DetailUserView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ["GET", "PUT", "DELETE"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
