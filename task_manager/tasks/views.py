import django.views.generic as generic
import django.contrib.auth.mixins as auth_mixins
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.filters import TaskFilter
from django_filters.views import FilterView


class TaskMixin(auth_mixins.LoginRequiredMixin):
    model = Task
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("tasks:list")


class TaskListView(
    TaskMixin,
    FilterView,
):
    template_name = "task_manager/tasks/list.html"
    filterset_class = TaskFilter


class TaskDetailView(
    TaskMixin,
    generic.DetailView
):
    template_name = "task_manager/tasks/detail.html"


class TaskCreateView(
    TaskMixin,
    generic.CreateView):
    form_class = TaskCreationForm
    template_name = "task_manager/tasks/form.html"
    extra_context = {
        "header": gettext_lazy("Create task"),
        "submit_button_label": gettext_lazy("Create")
    }
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request, gettext_lazy("User successfully registered")
        )
        return response


class TaskUpdateView(
    TaskMixin,
    generic.UpdateView
    ):
    form_class = TaskCreationForm
    template_name = "task_manager/tasks/form.html"
    extra_context = {
        "header": gettext_lazy("Edit task"),
        "submit_button_label": gettext_lazy("Edit")
    }
    


class TaskDeleteView(
    TaskMixin,
    auth_mixins.UserPassesTestMixin,
    generic.DeleteView
):
    template_name = "task_manager/tasks/delete.html"
    def test_func(self):
        return self.get_object().author == self.request.user
