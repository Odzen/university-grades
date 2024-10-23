from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import CourseViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet)
router.register("enrollments", EnrollmentViewSet)

urlpatterns = router.urls
