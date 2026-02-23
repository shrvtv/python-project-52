import django.views.generic as generic_views
from django.contrib.auth.models import User
from django.urls import reverse_lazy
import django.contrib.auth.mixins as mixins

from task_manager.users.forms import CustomUserCreationForm


class UserListView(generic_views.ListView):
    model = User
    queryset = User.objects.all()
    template_name = "task_manager/users/list.html"


class UserCreateView(generic_views.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/create.html"


class UserUpdateView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    generic_views.UpdateView
):
    pass


class UserDeleteView(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    generic_views.DeleteView
):
    model = User
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("index")
    template_name = "task_manager/users/delete.html"

    def test_func(self):
        return self.get_object() == self.request.user
