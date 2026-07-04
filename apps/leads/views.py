from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View
from django.http import JsonResponse

from apps.leads.models import Lead, LeadLog
from apps.leads.forms import LeadForm, LeadUpdateForm

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



class LeadCreateView(View):
    """
    Handle lead creation from dashboard modal.
    """

    def post(self, request, *args, **kwargs):
        form = LeadForm(request.POST)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()

            LeadLog.objects.create(
                lead=lead,
                created_by=request.user,
                message="Lead created.",
            )

            messages.success(
                request,
                "Lead created successfully.",
            )
        else:
            messages.error(
                request,
                "Please fill all required fields.",
            )

        return redirect("dashboard:home")
    

class LeadDetailView(View):

    def get(self, request, pk):

        lead = get_object_or_404(
            Lead.objects.select_related(
                "assigned_to",
                "created_by",
            ).prefetch_related("logs"),
            pk=pk,
        )

        data = {
            "id": lead.id,
            "full_name": lead.full_name,
            "phone_number": lead.phone_number,
            "locality": lead.locality,
            "budget": lead.budget,
            "bhk": lead.bhk,
            "priority": lead.priority,
            "status": lead.status,
            "assigned_to": (
                lead.assigned_to.get_full_name()
                if lead.assigned_to
                else ""
            ),
            "next_action": lead.next_action,
            "next_follow_up": (
                lead.next_follow_up.strftime("%d %b %Y")
                if lead.next_follow_up
                else ""
            ),
            "logs": [
                {
                    "message": log.message,
                    "created_by": (
                        log.created_by.get_full_name()
                        if log.created_by
                        else "System"
                    ),
                    "created_at": log.created_at.strftime("%d %b %Y %I:%M %p"),
                }
                for log in lead.logs.all()
            ],
        }

        return JsonResponse(data)
    

class LeadUpdateView(View):
    """
    Update lead information.
    """
    def post(self, request, pk):

        lead = get_object_or_404(
            Lead,
            pk=pk,
        )

        old_data = {
            "full_name": lead.full_name,
            "phone_number": lead.phone_number,
            "locality": lead.locality,
            "budget": lead.budget,
            "bhk": lead.bhk,
            "priority": lead.priority,
            "next_action": lead.next_action,
            "next_follow_up": str(lead.next_follow_up or ""),
        }

        form = LeadUpdateForm(
            request.POST,
            instance=lead,
        )

        if form.is_valid():

            updated_lead = form.save()

            # Create audit logs only for changed fields
            for field, old_value in old_data.items():

                new_value = str(getattr(updated_lead, field) or "")

                if str(old_value) != new_value:

                    LeadLog.objects.create(
                        lead=updated_lead,
                        created_by=request.user,
                        message=f"{field.replace('_', ' ').title()} changed from '{old_value}' to '{new_value}'.",
                    )

            return JsonResponse(
                {
                    "success": True,
                    "message": "Lead updated successfully.",
                }
            )

        return JsonResponse(
            {
                "success": False,
                "errors": form.errors,
            },
            status=400,
        )

    
class AddLeadLogView(View):
    """
    Create lead log.
    """
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)

        LeadLog.objects.create(
            lead=lead,
            created_by=request.user,
            message=request.POST["message"],
        )

        messages.success(
            request,
            "Log added successfully."
        )

        return redirect("dashboard:home")