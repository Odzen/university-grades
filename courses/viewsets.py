from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import CourseSerializer, EnrollmentSerializer
from .models import Course, Enrollment


class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing course instances.
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing enrollment instances.
    """

    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()
