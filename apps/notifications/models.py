from django.db import models
from apps.leads.models import Lead
from apps.accounts.models import User



class Notification(models.Model):

    class Type(models.TextChoices):
        LEAD_ASSIGNED = "LEAD_ASSIGNED", "Lead Assigned"
        LEAD_REASSIGNED = "LEAD_REASSIGNED", "Lead Reassigned"
        FOLLOW_UP = "FOLLOW_UP", "Follow-up"
        OVERDUE = "OVERDUE", "Overdue"
        SYSTEM = "SYSTEM", "System"

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    lead = models.ForeignKey(
        Lead,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=Type.choices,
    )
    
    action_url = models.CharField(
        max_length=255,
        blank=True,
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
