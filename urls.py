from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls, name="admin"),
    path("users/", include("task_manager.users.urls")),
    path("login/", views.AuthView.as_view(), name="login"),
    path("logout/", views.DeauthView.as_view(), name="logout"),
]
