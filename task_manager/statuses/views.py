import django.views.generic as views
import django.contrib.auth.mixins as mixins
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusCreationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

app_label = "statuses"


class StatusBaseView(mixins.LoginRequiredMixin):
    model = Status
    form_class = StatusCreationForm
    login_url = reverse_lazy("login")


class StatusCreateView(
    StatusBaseView,
    views.CreateView
):
    form_class = StatusCreationForm
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("statuses:list")
    template_name = "task_manager/statuses/form.html"
    extra_context = {
        "header": gettext_lazy("Create status"),
        "submit_button_label": gettext_lazy("Create")
    }


class StatusDeleteView(
    StatusBaseView,
    views.DeleteView
    
):
    pass


class StatusListView(
    StatusBaseView,
    views.ListView
):
    queryset = Status.objects.all()
    template_name = "task_manager/statuses/list.html"


class StatusUpdateView(
    StatusBaseView,
    views.UpdateView
):
    success_url = reverse_lazy("statuses:list")
    template_name = "task_manager/statuses/form.html"
    extra_context = {
        "header": gettext_lazy("Edit status"),
        "submit_button_label": gettext_lazy("Edit")
    }
