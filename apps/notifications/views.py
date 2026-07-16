from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Notification


class MarkNotificationReadView(View):
    """
    Mark a notification as read.
    """

    def post(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk,
            recipient=request.user,
        )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return JsonResponse(
            {
                "success": True,
            }
        )
    
class MarkAllNotificationsReadView(View):
    """
    Mark all notifications as read.
    """

    def post(self, request):

        Notification.objects.filter(
            recipient=request.user,
            is_read=False,
        ).update(
            is_read=True,
        )

        return JsonResponse(
            {
                "success": True,
                "message": "All notifications marked as read.",
            }
        )