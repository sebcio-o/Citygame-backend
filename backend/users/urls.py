from django.urls import path

from .views import AuthenticateUserView, CreateUserView

app_name = "users"

urlpatterns = [
    path("token/", AuthenticateUserView.as_view()),
    path("", CreateUserView.as_view()),
]
