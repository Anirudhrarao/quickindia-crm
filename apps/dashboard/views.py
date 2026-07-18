from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.leads.models import Lead
from apps.accounts.models import User
from apps.notifications.models import Notification
from django.utils import timezone
from apps.notifications.services import NotificationService




@login_required
def crm(request):
    """
    Render CRM dashboard.
    """
    NotificationService.generate_notifications(request.user)

    leads = (
        Lead.objects
        .select_related("assigned_to")
        .order_by("-created_at")
    )

    employees = User.objects.filter(
        is_active = True,
    ).order_by("first_name")

    notifications = (
        Notification.objects
        .filter(
            recipient=request.user,
            is_read=False,
        )
        .order_by("-created_at")[:10]
    )

    unread_notification_count = (
        Notification.objects
        .filter(
            recipient=request.user,
            is_read=False,
        )
        .count()
    )

    notification_data = []

    for notification in notifications:
        notification_data.append({
                "id": notification.id,
                "lead_id": notification.lead.id if notification.lead else None,
                "note": notification.message,
                "time": notification.created_at.strftime("%d %b %Y %I:%M %p"),
                "type": notification.notification_type.lower(),
            })
        
    today = timezone.localdate()

    followups_count = {
        "due_today": 0,
        "overdue": 0,
        "upcoming": 0,
        "none": 0,
    }

    for lead in leads:
        status = lead.get_follow_up_status()

        if status == "DUE_TODAY":
            followups_count["due_today"] += 1

        elif status == "OVERDUE":
            followups_count["overdue"] += 1

        elif status == "UPCOMING":
            followups_count["upcoming"] += 1

        else:
            followups_count["none"] += 1

    context = {
        "leads": leads,
        "employees": employees,
        "notifications": notification_data,
        "unread_notification_count": unread_notification_count,
        "followups_count": followups_count,
    }

    return render(request, "dashboard/crm.html", context)


