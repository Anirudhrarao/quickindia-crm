from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("<int:pk>/delete/",views.delete_lead,name="delete"),
    path("create/", views.LeadCreateView.as_view(), name="create"),
    path("<int:pk>/",views.LeadDetailView.as_view(),name="detail"),
    path("<int:pk>/update/",views.LeadUpdateView.as_view(),name="update"),
    path("<int:pk>/add-log/",views.AddLeadLogView.as_view(),name="add_log"),
    path("<int:pk>/status/",views.LeadStatusUpdateView.as_view(),name="status_update"),
    path("<int:pk>/assign/",views.LeadAssignView.as_view(),name="assign"),
]