from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import DashboardView


app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]