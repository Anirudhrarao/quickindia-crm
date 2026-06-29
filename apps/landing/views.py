from django.shortcuts import render


def home(request):
    """
    Render landing page.
    """
    return render(request, "landing/index.html")