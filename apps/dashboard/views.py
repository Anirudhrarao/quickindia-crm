from django.shortcuts import render


def crm(request):
    """
    Render CRM dashboard.
    """
    return render(request, "dashboard/crm.html")