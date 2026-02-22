import django.views.generic as generic_views
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from task_manager.users.forms import CustomUserCreationForm


class UserListView(generic_views.ListView):
    model = User
    queryset = User.objects.all()
    template_name = "task_manager/users/list.html"


class UserCreateView(generic_views.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/create.html"


class UserUpdateView(generic_views.UpdateView):
    pass


class UserDeleteView(generic_views.DeleteView):
    pass
