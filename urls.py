from django.urls import path, include

urlpatterns = [
    path("", include("task_manager.urls")),
    
]
