from django.contrib.auth.models import User
from django.db.models.deletion import RestrictedError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, get_object_or_404

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .serializers import RegisterUserSerializer, AuthenticateUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken


@extend_schema_view(post=extend_schema(summary="Create user"))
class CreateUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed("User not logged in")
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


@extend_schema_view(
    post=extend_schema(summary="Get user tokens", request=AuthenticateUserSerializer)
)
class AuthenticateUserView(ObtainAuthToken):
    serializer_class = AuthenticateUserSerializer