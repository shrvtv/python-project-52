import django.views.generic as generic_views
from django.contrib.auth.models import User
from django.urls import reverse_lazy
import django.contrib.auth.mixins as mixins
from django.utils.translation import gettext_lazy
from task_manager.users.forms import CustomUserCreationForm


class UserMixin:
    model = User
    login_url = reverse_lazy("login")
    def test_func(self):
        return self.get_object() == self.request.user


class UserCreateView(
    UserMixin,
    generic_views.CreateView,
    ):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/form.html"
    extra_context = {
        "header": gettext_lazy("Registration"),
        "submit_button_label": gettext_lazy("Sign up")
    }


class UserDeleteView(
    UserMixin,
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    generic_views.DeleteView,
):
    success_url = reverse_lazy("index")
    template_name = "task_manager/users/delete.html"


class UserListView(
    UserMixin,
    generic_views.ListView,
    ):
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/list.html"


class UserUpdateView(
    UserMixin,
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
    generic_views.UpdateView,
):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/form.html"
    extra_context = {
        "header": gettext_lazy("Edit user"),
        "submit_button_label": gettext_lazy("Modify")
        }
