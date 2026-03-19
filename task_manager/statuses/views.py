import django.contrib.auth.mixins as mixins
import django.views.generic as views
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy

from task_manager.statuses.forms import StatusCreationForm
from task_manager.statuses.models import Status

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

    def form_valid(self, form):
        messages.success(
            self.request, gettext_lazy("Status successfully created")
        )
        return super().form_valid(form)


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

    def form_valid(self, form):
        messages.success(
            self.request, gettext_lazy("Status successfully updated")
        )
        return super().form_valid(form)


class StatusDeleteView(
    StatusMixin,
    views.DeleteView,
):
    template_name = "task_manager/statuses/delete.html"
    
    def form_valid(self, form):
        if self.get_object().tasks_assigned.exists():
            messages.error(
                self.request, gettext("Cannot delete a status in use")
            )
            return redirect("statuses:list")
        messages.success(self.request, gettext("Status successfully deleted"))
        return super().form_valid(form)
