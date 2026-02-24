import django.views.generic as views
import django.contrib.auth.mixins as mixins
from task_manager.statuses.models import Status


class StatusCreateView(
    mixins.LoginRequiredMixin,
    views.CreateView
):
    pass


class StatusDeleteView(
    mixins.LoginRequiredMixin,
    views.DeleteView
):
    model = Status


class StatusListView(
    mixins.LoginRequiredMixin,
    views.ListView
):
    model = Status


class StatusUpdateView(
    mixins.LoginRequiredMixin,
    views.UpdateView
):
    model = Status
