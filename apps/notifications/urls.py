from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [

    path("<int:pk>/read/",views.MarkNotificationReadView.as_view(),name="read"),
    path("read-all/",views.MarkAllNotificationsReadView.as_view(),name="read_all"),
]