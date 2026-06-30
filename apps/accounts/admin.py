from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for custom user model.
    """

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "phone_number",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "QuickIndia CRM",
            {
                "fields": (
                    "role",
                    "phone_number",
                    "profile_image",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "QuickIndia CRM",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                    "phone_number",
                ),
            },
        ),
    )