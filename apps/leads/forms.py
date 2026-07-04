from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    """
    Form used by the Add Lead popup.
    """

    class Meta:
        model = Lead
        fields = (
            "full_name",
            "phone_number",
            "assigned_to",
            "locality",
            "bhk",
            "budget",
            "priority",
        )

class LeadUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "full_name",
            "phone_number",
            "locality",
            "budget",
            "bhk",
            "priority",
            "next_action",
            "next_follow_up",
        )