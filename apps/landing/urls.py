from django.urls import path

from . import views

app_name = "landing"

urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "properties/",
        views.PropertyListView.as_view(),
        name="property_list",
    ),

    path(
        "property/create/",
        views.PropertyCreateView.as_view(),
        name="property_create",
    ),

    path(
        "property/<int:pk>/",
        views.PropertyDetailView.as_view(),
        name="property_detail",
    ),

    path(
        "property/<int:pk>/update/",
        views.PropertyUpdateView.as_view(),
        name="property_update",
    ),

    path(
        "property/<int:pk>/delete/",
        views.PropertyDeleteView.as_view(),
        name="property_delete",
    ),
]