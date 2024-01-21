from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from users.models.user import User


class BlockedUser(BaseModel):
    """
    Model to store information about blocked and deleted users.

    This model represents a record of users who have been blocked and deleted
    from the system. It includes information such as the blocked user, the reason
    for blocking, and the user who performed the block action.

    Attributes:
    - `user`: ForeignKey to the User model, representing the blocked user.
    - `blocked_reason`: A string field describing the reason for blocking.
    - `blocked_by`: ForeignKey to the User model, representing the user who blocked.

    Meta:
    - `verbose_name`: "Blocked and Deleted User"
    - `verbose_name_plural`: "Blocked and Deleted Users"
    - `db_table`: "BlockedUser"

    Methods:
    - `__str__`: Returns a string representation of the blocked user.

    Example:
    ```
    blocked_user = BlockedUser.objects.create(
        user=user_instance,
        blocked_reason="Violating community guidelines",
        blocked_by=admin_user_instance
    )
    ```

    Note: This model is used to keep a record of blocked and deleted users in the system.
    """

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="blocked_users",
    )
    blocked_reason = models.CharField(max_length=255, verbose_name=_("Reason"), blank=False)
    blocked_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Blocked By"),
        related_name="blocked",
    )

    class Meta:
        verbose_name = _("Blocked and Deleted User")
        verbose_name_plural = _("Blocked and Deleted Users")
        db_table = "BlockedUser"

    def __str__(self):
        return str(self.user)

    def delete(self, using=None, keep_parents=False):
        if self.user and self.user.is_blocked:
            self.user.is_blocked = False
            self.user.save()

        if self.user and self.user.is_deleted:
            self.user.is_deleted = False
            self.user.save()
        return super().delete(using, keep_parents)
