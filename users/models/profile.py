from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, Media
from users.models.user import User


class UserProfile(BaseModel):
    """
    Model to store user profile information.

    This model represents a user's profile, storing additional information such
    as a profile image, address, postal code, and whether the user has agreed to
    terms and conditions.

    Attributes:
    - `user`: One-to-one relationship with the User model.
    - `profile_image`: One-to-one relationship with the Media model, representing
      the user's profile image.
    - `address`: A string field for storing the user's address.
    - `postal_code`: A string field for storing the user's postal code.
    - `is_agree_to_terms_and_condition`: A boolean field indicating whether the user
      has agreed to terms and conditions.

    Methods:
    - `__str__`: Returns a string representation of the user profile.
    - `get_profile_image_path`: Returns the URL of the user's profile image, if available.

    Meta:
    - `verbose_name`: "User Profile"
    - `verbose_name_plural`: "Manage Users Profile"
    - `db_table`: "UserProfile"

    Example:
    ```
    user_profile = UserProfile.objects.create(
        user=user_instance,
        profile_image=media_instance,
        address="123 Main Street",
        postal_code="123456",
        is_agree_to_terms_and_condition=True
    )
    ```

    Note: This model is used to store additional information about a user's profile.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("User"))
    profile_image = models.OneToOneField(
        Media,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_profile_image",
        verbose_name=_("Profile Image"),
    )
    address = models.CharField(max_length=255, default="", blank=True, verbose_name=_("Address"))
    postal_code = models.CharField(max_length=6, default="", blank=True, verbose_name=_("Postal Code"))
    is_agree_to_terms_and_condition = models.BooleanField(
        default=False, verbose_name=_("Has agreed to terms & condition")
    )

    def __str__(self):
        return f"UserProfile for {self.user}"

    def get_profile_image_path(self):
        if self.profile_image:
            return self.profile_image.file_path.url
        return None

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Manage Users Profile"
        db_table = "UserProfile"
