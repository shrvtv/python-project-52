import django.views.generic as generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy
from django_filters.views import FilterView

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskMixin(LoginRequiredMixin):
    model = Task
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("tasks:list")


class TaskCreateView(
    TaskMixin,
    generic.CreateView,
):
    form_class = TaskForm
    template_name = "task_manager/tasks/form.html"
    extra_context = {
        "header": gettext_lazy("Create task"),
        "submit_button_label": gettext_lazy("Create")
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request, gettext("Task successfully created")
        )
        return super().form_valid(form)


class TaskListView(
    TaskMixin,
    FilterView,
):
    template_name = "task_manager/tasks/list.html"
    filterset_class = TaskFilter


class TaskDetailView(
    TaskMixin,
    generic.DetailView,
):
    template_name = "task_manager/tasks/detail.html"


class TaskUpdateView(
    TaskMixin,
    generic.UpdateView,
):
    form_class = TaskForm
    template_name = "task_manager/tasks/form.html"
    extra_context = {
        "header": gettext_lazy("Edit task"),
        "submit_button_label": gettext_lazy("Edit")
    }

    def form_valid(self, form):
        messages.success(
            self.request, gettext("Task successfully updated")
        )
        return super().form_valid(form)


class TaskDeleteView(
    TaskMixin,
    UserPassesTestMixin,
    generic.DeleteView,
):
    template_name = "task_manager/tasks/delete.html"

    def form_valid(self, form):
        messages.success(
            self.request, gettext("Task successfully deleted")
        )
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        messages.error(self.request, gettext("Only owner can delete the task"))
        return redirect("tasks:list")
