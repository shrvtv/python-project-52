import django.views.generic as generic
import django.contrib.auth.mixins as auth_mixins
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskCreationForm, TaskFilterForm


class TaskMixin(auth_mixins.LoginRequiredMixin):
    model = Task
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("tasks:list")


class TaskListView(
    TaskMixin,
    generic.ListView
):
    template_name = "task_manager/tasks/list.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["form"] = TaskFilterForm({
            "status": self.request.GET.get("status"),
            "executor": self.request.GET.get("executor"),
            "self_tasks": self.request.GET.get("self_tasks")
        })
        return data

    def get_queryset(self):
        tasks = Task.objects.all()
        if self.request.GET.get("self_tasks"):
            tasks = tasks.filter(author_id=self.request.user.pk)
        status_id = self.request.GET.get("status")
        if status_id:
            tasks = tasks.filter(status_id=status_id)
        executor_id = self.request.GET.get("executor")
        if executor_id:
            tasks = tasks.filter(executor_id=executor_id)
        return tasks


class TaskDetailView(generic.DetailView):
    pass


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
        return super().form_valid(form)


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
