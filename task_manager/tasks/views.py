import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskCreationForm


class TaskMixin(LoginRequiredMixin):
    model = Task
    login_url = reverse_lazy("login")


class TaskListView(
    TaskMixin,
    generic.ListView
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["users"] = User.objects.all()
        return context
    template_name = "task_manager/tasks/list.html"


class TaskDetailView(generic.DetailView):
    pass


class TaskCreateView(generic.CreateView):
    form_class = TaskCreationForm
    success_url = reverse_lazy("tasks:list")
    template_name = "task_manager/tasks/form.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(generic.UpdateView):
    pass


class TaskDeleteView(generic.DeleteView):
    pass
