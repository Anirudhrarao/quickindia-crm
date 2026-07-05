from .models import Notification


class NotificationService:
    """
    Handles notification creation.
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
        Create a notification.
        """
        Notification.objects.create(
            recipient=recipient,
            lead=lead,
            title=title,
            message=message,
            notification_type=notification_type,
            action_url=action_url,
        )
        