from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel
from users.managers.user import UserManager


class User(BaseModel, AbstractUser):
    """
    Custom user model extending AbstractUser and BaseModel.

    This model represents a user in the system. It extends the default Django
    AbstractUser and includes additional fields like email, mobile number, and
    custom manager.

    Attributes:
    - `email`: Email address of the user (unique).
    - `mobile_number`: Mobile number of the user (unique).
    - `phone_code`: Country phone code for the user's mobile number.
    - `is_deleted`: Indicates whether the user is deleted.
    - `is_blocked`: Indicates whether the user is blocked.
    - `is_superuser`: Indicates whether the user has superuser/admin privileges.

    Methods:
    - `__str__`: Returns a string representation of the user.

    Meta:
    - `verbose_name`: "User"
    - `verbose_name_plural`: "Manage Users"
    - `db_table`: "User"

    Example:
    ```
    user = User.objects.create(email="user@example.com", password="securepassword")
    ```

    Note: The `USERNAME_FIELD` is set to "email" for authentication.
    """

    username = None

    email = models.EmailField(verbose_name=_("Email Address"), blank=True, unique=True, null=True, db_column="email")

    mobile_number = models.CharField(
        verbose_name=_("Mobile Number"), max_length=13, blank=True, default="", unique=True, db_column="mobile_number"
    )
    phone_code = models.CharField(
        verbose_name=_("Phone Code"),
        max_length=5,
        db_column="phone_code",
        default="+1",
        help_text=_("Enter the country phone code."),
    )

    is_deleted = models.BooleanField(
        verbose_name=_("Is Deleted?"),
        default=False,
        db_column="deleted",
    )

    is_blocked = models.BooleanField(
        verbose_name=_("Is Blocked?"),
        default=False,
        db_column="blocked",
    )

    is_superuser = models.BooleanField(_("Is Admin?"), default=False, db_column="is_superuser")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name:
            return self.first_name
        elif self.email:
            return self.email
        elif self.mobile_number:
            return self.mobile_number
        return self.pk

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Manage Users"
        db_table = "User"
