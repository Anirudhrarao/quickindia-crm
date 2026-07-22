from django.db import models


class Property(models.Model):
    """
    Featured property shown on the landing page.
    """

    class PropertyType(models.TextChoices):
        APARTMENT = "APARTMENT", "Apartment"
        VILLA = "VILLA", "Villa"
        PENTHOUSE = "PENTHOUSE", "Penthouse"
        PLOT = "PLOT", "Plot"
        OFFICE = "OFFICE", "Office"
        SHOP = "SHOP", "Shop"

    image = models.ImageField(
        upload_to="properties/",
    )

    title = models.CharField(
        max_length=150,
    )

    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    location = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    bedrooms = models.PositiveIntegerField(
        default=0,
    )

    bathrooms = models.PositiveIntegerField(
        default=0,
    )

    area_sqft = models.PositiveIntegerField(
        help_text="Area in square feet",
    )

    is_rera_compliant = models.BooleanField(
        default=True,
    )

    display_order = models.PositiveIntegerField(
        default=1,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "display_order",
            "-created_at",
        ]

    def __str__(self):
        return self.title