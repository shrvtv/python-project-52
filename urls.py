from django.urls import include, path

urlpatterns = [
    path("", include("task_manager.urls")),
    
]
