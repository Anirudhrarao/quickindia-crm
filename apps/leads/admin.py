from django.contrib import admin

from .models import Lead, LeadLog


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """
    Admin configuration for Lead model.
    """

    list_display = (
        "full_name",
        "phone_number",
        "locality",
        "budget",
        "assigned_to",
        "status",
        "priority",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone_number",
        "email",
        "locality",
    )

    readonly_fields = (
        "created_by",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        """
        Automatically set the creator when a lead is created.
        """
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    autocomplete_fields = (
        "assigned_to",
        "created_by",
    )

    ordering = ("-created_at",)

    list_select_related = (
        "assigned_to",
        "created_by",
    )

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "full_name",
                    "phone_number",
                    "email",
                )
            },
        ),
        (
            "Property Requirement",
            {
                "fields": (
                    "locality",
                    "budget",
                    "bhk",
                )
            },
        ),
        (
            "Lead Information",
            {
                "fields": (
                    "assigned_to",
                    "status",
                    "priority",
                    "next_action",
                    "next_follow_up",
                    "notes",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(LeadLog)
class LeadLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for LeadLog model.
    """

    list_display = (
        "lead",
        "created_by",
        "created_at",
    )

    search_fields = (
        "lead__full_name",
        "message",
    )

    autocomplete_fields = (
        "lead",
        "created_by",
    )
    
    list_select_related = (
        "lead",
        "created_by",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = ("-created_at",)

    