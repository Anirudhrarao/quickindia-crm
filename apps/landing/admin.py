from django.contrib import admin
from django.utils.html import format_html

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Admin configuration for featured properties.
    """

    list_display = (
        "image_preview",
        "title",
        "property_type",
        "price",
        "location",
        "bedrooms",
        "bathrooms",
        "area_sqft",
        "is_rera_compliant",
        "is_active",
        "display_order",
    )

    list_filter = (
        "property_type",
        "is_rera_compliant",
        "is_active",
    )

    search_fields = (
        "title",
        "location",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
        "updated_at",
    )

    ordering = (
        "display_order",
        "-created_at",
    )

    fieldsets = (
        (
            "Property Details",
            {
                "fields": (
                    "title",
                    "property_type",
                    "price",
                    "location",
                    "description",
                )
            },
        ),
        (
            "Property Image",
            {
                "fields": (
                    "image",
                    "image_preview",
                )
            },
        ),
        (
            "Property Specifications",
            {
                "fields": (
                    "bedrooms",
                    "bathrooms",
                    "area_sqft",
                    "is_rera_compliant",
                )
            },
        ),
        (
            "Display Settings",
            {
                "fields": (
                    "display_order",
                    "is_active",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50"    style="border-radius:8px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Preview"