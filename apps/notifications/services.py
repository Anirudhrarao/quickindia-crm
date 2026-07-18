from datetime import timedelta
from django.utils import timezone
from .models import Notification
from apps.leads.models import Lead


class NotificationService:
    """
    Handles all notification creation.
    """

    @staticmethod
    def create(
        recipient,
        title,
        message,
        notification_type,
        lead=None,
        action_url="",
    ):
        """
        Create notification if an unread notification of the same
        type doesn't already exist.
        """

        notification = Notification.objects.filter(
            recipient=recipient,
            lead=lead,
            notification_type=notification_type,
            is_read=False,
        ).first()

        if notification:
            return notification

        return Notification.objects.create(
            recipient=recipient,
            lead=lead,
            title=title,
            message=message,
            notification_type=notification_type,
            action_url=action_url,
        )

    @staticmethod
    def exists(recipient, lead, notification_type):
        """
        Check if unread notification already exists.
        """

        return Notification.objects.filter(
            recipient=recipient,
            lead=lead,
            notification_type=notification_type,
            is_read=False,
        ).exists()

    @staticmethod
    def mark_old_followups_read(lead):
        """
        Mark all previous follow-up notifications as read.

        NOTE:
        This should ONLY be called when the follow-up date
        is changed by the user.
        """

        Notification.objects.filter(
            lead=lead,
            notification_type__in=[
                Notification.Type.FOLLOW_UP,
                Notification.Type.OVERDUE,
            ],
            is_read=False,
        ).update(is_read=True)

    @staticmethod
    def sync_lead_notifications(lead):
        """
        Generate notification according to follow-up date.

        Rules:

        Tomorrow  -> FOLLOW_UP
        Today     -> FOLLOW_UP
        Overdue   -> OVERDUE (one notification per day)
        """

        if not lead.assigned_to:
            return

        if not lead.next_follow_up:
            return

        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        # -----------------------------
        # Tomorrow Reminder
        # -----------------------------
        if lead.next_follow_up == tomorrow:

            if not NotificationService.exists(
                lead.assigned_to,
                lead,
                Notification.Type.FOLLOW_UP,
            ):

                NotificationService.create(
                    recipient=lead.assigned_to,
                    lead=lead,
                    title="Follow-up Tomorrow",
                    message=f"{lead.full_name} needs follow-up tomorrow.",
                    notification_type=Notification.Type.FOLLOW_UP,
                    action_url=f"/crm/leads/{lead.id}/",
                )

            return

        # -----------------------------
        # Today's Follow-up
        # -----------------------------
        if lead.next_follow_up == today:

            if not NotificationService.exists(
                lead.assigned_to,
                lead,
                Notification.Type.FOLLOW_UP,
            ):

                NotificationService.create(
                    recipient=lead.assigned_to,
                    lead=lead,
                    title="Today's Follow-up",
                    message=f"Follow up with {lead.full_name} today.",
                    notification_type=Notification.Type.FOLLOW_UP,
                    action_url=f"/crm/leads/{lead.id}/",
                )

            return

        # -----------------------------
        # Overdue
        # One notification per day
        # -----------------------------
        if lead.next_follow_up < today:

            already_created_today = Notification.objects.filter(
                recipient=lead.assigned_to,
                lead=lead,
                notification_type=Notification.Type.OVERDUE,
                created_at__date=today,
            ).exists()

            if not already_created_today:

                Notification.objects.create(
                    recipient=lead.assigned_to,
                    lead=lead,
                    title="Overdue Follow-up",
                    message=f"{lead.full_name} follow-up is overdue.",
                    notification_type=Notification.Type.OVERDUE,
                    action_url=f"/crm/leads/{lead.id}/",
                )


    @staticmethod
    def generate_notifications(user):
        """
        Generate follow-up notifications for the logged-in user.

        Runs whenever the dashboard loads.
        """

        if not user.is_authenticated:
            return

        leads = Lead.objects.filter(
            assigned_to=user,
        ).only(
            "id",
            "full_name",
            "next_follow_up",
            "assigned_to",
        )

        for lead in leads:
            NotificationService.sync_lead_notifications(lead)