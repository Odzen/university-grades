from django.contrib import admin
from django.urls import path, include

from users.urls import urlpatterns as user_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include(user_urlpatterns)),
]
