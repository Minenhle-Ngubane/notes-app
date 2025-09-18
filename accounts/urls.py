from django.urls import path

from .views import RegisterView, LoginView, LogoutView, UpdateUserView


app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("update/", UpdateUserView.as_view(), name="update"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]