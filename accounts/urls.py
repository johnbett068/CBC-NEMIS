# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"  # <-- THIS is the namespace

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]
