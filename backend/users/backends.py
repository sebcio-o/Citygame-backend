from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


class AuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):

        username = kwargs.get("username")
        if (not email and not username) or not password:
            return

        user = User.objects.filter(Q(email=email) | Q(username=username)).first()
        if not user:
            User().set_password(password)
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


backend = AuthBackend()
