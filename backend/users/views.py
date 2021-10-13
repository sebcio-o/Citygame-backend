from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import AuthenticateUserSerializer, RegisterUserSerializer


@extend_schema_view(post=extend_schema(summary="Create user"))
class CreateUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


@extend_schema_view(
    post=extend_schema(summary="Get user tokens", request=AuthenticateUserSerializer)
)
class AuthenticateUserView(ObtainAuthToken):
    serializer_class = AuthenticateUserSerializer
