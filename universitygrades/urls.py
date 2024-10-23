from django.contrib import admin
from django.urls import path, include

from users.urls import urlpatterns as user_urlpatterns
from subjects.urls import urlpatterns as subject_urlpatterns
from courses.urls import urlpatterns as course_urlpatterns
from docs.urls import urlpatterns as docs_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(user_urlpatterns)),
    path("", include(subject_urlpatterns)),
    path("", include(course_urlpatterns)),
    path("docs/", include(docs_urlpatterns)),
]
