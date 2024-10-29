from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from courses.urls import urlpatterns as course_urlpatterns
from subjects.urls import urlpatterns as subject_urlpatterns
from users.urls import auth_urlpatterns as auth_urlpatterns
from users.urls import users_urlpatterns as user_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(user_urlpatterns)),
    path("auth/", include(auth_urlpatterns)),
    path("", include(subject_urlpatterns)),
    path("", include(course_urlpatterns)),
    path("docs/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
]
