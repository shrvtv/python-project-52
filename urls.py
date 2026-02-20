from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from views import index

urlpatterns = [
    path("", index),
    path('admin/', admin.site.urls, name="admin"),
    path("users/", include("task_manager.users.urls")),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
