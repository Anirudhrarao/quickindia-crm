from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.leads.models import Lead
from apps.accounts.models import User




@login_required
def crm(request):
    """
    Render CRM dashboard.
    """
    leads = (
        Lead.objects
        .select_related("assigned_to")
        .order_by("-created_at")
    )

    employees = User.objects.filter(
        is_active = True,
    ).order_by("first_name")

    context = {
        "leads": leads,
        "employees": employees
    }

    return render(request, "dashboard/crm.html", context)


