from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import CustomUser


class MultiFieldAuthBackend(ModelBackend):
    """
    Custom authentication backend allowing users to log in with:
    - Username
    - Admission Number (especially for UniSmart & Campus students)
    - Email Address
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
            
        identifier = str(username).strip()
        if not identifier:
            return None

        try:
            # Match by username, admission_number, or non-empty email
            user = CustomUser.objects.filter(
                Q(username__iexact=identifier) |
                Q(admission_number__iexact=identifier) |
                (Q(email__iexact=identifier) & ~Q(email=''))
            ).first()

            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None

        return None
