from django.conf import settings
from django.db import models
from django.utils import timezone

class Lead(models.Model):
    """
    Stores customer lead information.
    """
    def get_follow_up_status(self):
        """
        Returns:
            NO_FOLLOW_UP
            UPCOMING
            DUE_TODAY
            OVERDUE
        """

        if not self.next_follow_up:
            return "NO_FOLLOW_UP"

        today = timezone.localdate()

        if self.next_follow_up < today:
            return "OVERDUE"

        if self.next_follow_up == today:
            return "DUE_TODAY"

        return "UPCOMING"


    def is_overdue(self):
        return self.get_follow_up_status() == "OVERDUE"


    def is_due_today(self):
        return self.get_follow_up_status() == "DUE_TODAY"


    def is_upcoming(self):
        return self.get_follow_up_status() == "UPCOMING"


    def has_follow_up(self):
        return self.next_follow_up is not None
    
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
    

class LeadLog(models.Model):
    """
    Stores the activity timeline of a lead.
    """

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="logs",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.lead.full_name} - {self.created_at:%d %b %Y}"