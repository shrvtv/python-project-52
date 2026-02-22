import task_manager.users.views as user_views
from django.urls import path

app_name = "users"

urlpatterns = [
    path("", user_views.UserListView.as_view(), name="list"),
    path("create/", user_views.UserCreateView.as_view(), name="create"),
    path("<int:pk>/update/", user_views.UserUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", user_views.UserDeleteView.as_view(), name="delete")
]
