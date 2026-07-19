from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from src.apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""

    list_display = (
        "email",
        "username",
        "is_staff",
        "is_active",
        "email_verified",
        "date_joined",
    )
    list_filter = ("is_staff", "is_active", "email_verified", "theme")
    search_fields = ("email", "username", "phone_number")
    ordering = ("-date_joined",)
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": (
                    "phone_number",
                    "bio",
                    "avatar",
                    "date_of_birth",
                    "email_verified",
                    "is_online",
                    "last_activity",
                )
            },
        ),
        ("Preferences", {"fields": ("email_notifications", "theme")}),
    )
