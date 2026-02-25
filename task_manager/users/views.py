import django.views.generic as generic_views
from django.contrib.auth.models import User
from django.urls import reverse_lazy
import django.contrib.auth.mixins as mixins
from django.utils.translation import gettext_lazy
from task_manager.users.forms import CustomUserCreationForm


class UserBaseView:
    login_url = reverse_lazy("login")
    def test_func(self):
        return self.get_object() == self.request.user

class UserCreateView(
    generic_views.CreateView,
    UserBaseView,
    ):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/form.html"
    extra_context = {
        "header": gettext_lazy("Registration"),
        "submit_button_label": gettext_lazy("Sign up")
    }


class UserDeleteView(
    generic_views.DeleteView,
    UserBaseView,
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
):
    model = User
    success_url = reverse_lazy("index")
    template_name = "task_manager/users/delete.html"


class UserListView(
    generic_views.ListView,
    UserBaseView,
    ):
    model = User
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/list.html"


class UserUpdateView(
    generic_views.UpdateView,
    UserBaseView,
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin,
):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/form.html"
    extra_context = {
        "header": gettext_lazy("Edit user"),
        "submit_button_label": gettext_lazy("Modify")
        }
