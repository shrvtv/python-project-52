import task_manager.users.views as views
from django.urls import path


urlpatterns = [
    path("", views.UsersIndex.as_view(), name="users")
]
