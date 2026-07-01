from django.conf import settings
from django.db import models


class Lead(models.Model):
    """
    Stores customer lead information.
    """

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CALLED = "CALLED", "Called"
        INTERESTED = "INTERESTED", "Interested"
        SITE_VISIT = "SITE_VISIT", "Site Visit Scheduled"
        CLOSED = "CLOSED", "Closed"

    class Priority(models.TextChoices):
        HOT = "HOT", "Hot"
        WARM = "WARM", "Warm"
        COLD = "COLD", "Cold"

    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    locality = models.CharField(max_length=150)
    budget = models.CharField(max_length=100)
    bhk = models.CharField(max_length=20)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.WARM,
    )

    next_follow_up = models.DateField(
        blank=True,
        null=True,
    )

    next_action = models.CharField(
        max_length=255,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_leads",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name