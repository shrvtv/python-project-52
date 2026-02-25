import django.views.generic as views
import django.contrib.auth.mixins as mixins
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusCreationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

app_label = "statuses"


class StatusMixin(mixins.LoginRequiredMixin):
    model = Status
    login_url = reverse_lazy("login")
    def get_success_url(self):
        return reverse_lazy("statuses:list")


class StatusCreateView(
    StatusMixin,
    views.CreateView,
):
    form_class = StatusCreationForm
    template_name = "task_manager/statuses/form.html"
    extra_context = {
        "header": gettext_lazy("Create status"),
        "submit_button_label": gettext_lazy("Create")
    }


class StatusDeleteView(
    StatusMixin,
    views.DeleteView,
):
    template_name = "task_manager/statuses/delete.html"


class StatusListView(
    StatusMixin,
    views.ListView,
):
    template_name = "task_manager/statuses/list.html"


class StatusUpdateView(
    StatusMixin,
    views.UpdateView,
):
    form_class = StatusCreationForm
    template_name = "task_manager/statuses/form.html"
    extra_context = {
        "header": gettext_lazy("Edit status"),
        "submit_button_label": gettext_lazy("Edit")
    }
