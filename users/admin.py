from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import CustomModelAdmin
from users.models import User, UserProfile


# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1


class UserAdmin(CustomModelAdmin):
    inlines = [
        UserProfileInline,
    ]
    empty_value_display = "-empty-"
    fieldsets = [
        (
            _("Details"),
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "email",
                    "phone_code",
                    "mobile_number",
                    "password",
                ]
            },
        ),
        (
            _("Permissions"),
            {
                "fields": [
                    "is_active",
                    "is_superuser",
                ]
            },
        ),
        (
            _("Additional Information"),
            {
                "fields": [
                    "last_login",
                    "date_joined",
                ]
            },
        ),
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": [
                    "first_name",
                    "last_name",
                    "mobile_number",
                    "password1",
                    "password2",
                ],
            },
        ),
    )
    exclude = ["username"]
    readonly_fields = [
        "is_superuser",
        "last_login",
        "date_joined",
    ]
    list_display = [
        "created",
        "first_name",
        "last_name",
        "email",
        "mobile_number",
    ]
    list_display_links = ["email", "mobile_number"]
    ordering = ["first_name", "last_name", "email"]
    list_filter = ["is_superuser", "blocked"]


admin.site.register(User, UserAdmin)
