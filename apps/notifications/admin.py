from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notification model.
    """

    list_display = (
        "title",
        "recipient",
        "notification_type",
        "lead",
        "action_url",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
        "action_url",
        "recipient__first_name",
        "recipient__last_name",
        "recipient__username",
        "lead__full_name",
    )

    autocomplete_fields = (
        "recipient",
        "lead",
    )

    readonly_fields = (
        "created_at",
    )

    list_select_related = (
        "recipient",
        "lead",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Notification Information",
            {
                "fields": (
                    "title",
                    "message",
                    "notification_type",
                    "action_url",
                )
            },
        ),
        (
            "Recipient",
            {
                "fields": (
                    "recipient",
                    "lead",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_read",
                    "created_at",
                )
            },
        ),
    )

