from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.leads.models import Lead


def delete_lead(request, pk):
    """
    Delete a lead.
    """
    lead = get_object_or_404(
        Lead,
        pk=pk,
    )

    lead.delete()

    messages.success(
        request,
        "Lead deleted successfully."
    )

    return redirect("dashboard:home")