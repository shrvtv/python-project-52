from django.urls import path

import task_manager.statuses.views as status_views

app_name = "statuses"

urlpatterns = [
    path("", status_views.StatusListView.as_view(), name="list"),
    path("create/", status_views.StatusCreateView.as_view(), name="create"),
    path("<int:pk>/update/", status_views.StatusUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", status_views.StatusDeleteView.as_view(), name="delete"),
]
