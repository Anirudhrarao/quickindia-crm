from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("<int:pk>/delete/",views.delete_lead,name="delete"),
]