from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import RegisterView, LoginView, UpdateUserView


app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("update/", UpdateUserView.as_view(), name="update"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]