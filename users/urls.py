from django.urls import path

from .views import ListUsersView, DetailUserView


urlpatterns = [
    path("", view=ListUsersView.as_view()),
    path("<int:user_id>/", view=DetailUserView.as_view()),
]
