from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm

def login_view(request):
    """
    Authenticate and log in a user.
    """

    if request.user.is_authenticated:
        return redirect("dashboard:home")
    
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect("dashboard:home")
            
            messages.error(request, "Invalid username or password.")
    
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """
    Logout current user.
    """
    logout(request)
    messages.success(request, "Logged out successfully.")

    return redirect("accounts:login")