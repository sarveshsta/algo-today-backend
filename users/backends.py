from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q


# Custom Authentication Backend
class MobileOrEmailBackend(BaseBackend):
    """
    class MobileorEmailBackend is called by the django auth.
    Whenever we sign up or sign this class is invoke to
    authenticate the user.

    This class require two method implementation
    `authenticate` and `get_user`

    """

    def authenticate(self, identifier=None, phone_code=None, **kwargs):
        user_modal = get_user_model()
        try:
            # Try to fetch the user by searching the username or email field
            user = user_modal.objects.filter(phone_code=phone_code).get(
                Q(mobile_number=identifier) | Q(email__iexact=identifier)
            )
            if user.is_active:
                return user
        except user_modal.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user.
            pass

    def get_user(self, user_id):
        user_modal = get_user_model()
        try:
            return user_modal.objects.get(pk=user_id)
        except user_modal.DoesNotExist:
            return None
