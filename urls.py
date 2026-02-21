from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("task_manager.urls")),
    
]
