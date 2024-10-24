from .serializers import UserSerializer, RegisterSerializer
from .models import User
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


# Auth
class SignupView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        return Response(UserSerializer(user).data)


class ListUsersView(ListAPIView, CreateAPIView):
    """
    Get all users or create a new user
    """

    allowed_methods = ["GET", "POST"]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class DetailUserView(RetrieveUpdateDestroyAPIView):
    allowed_methods = ["GET", "PUT", "DELETE"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
