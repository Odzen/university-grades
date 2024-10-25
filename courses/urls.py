from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import CourseViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet)

urlpatterns = router.urls
