from django.urls import path

from .views import CreateUserView, AuthenticateUserView

app_name = "users"

urlpatterns = [
    path("token/", AuthenticateUserView.as_view()),
    path("", CreateUserView.as_view()),
]
