from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def crm(request):
    """
    Render CRM dashboard.
    """
    return render(request, "dashboard/crm.html")