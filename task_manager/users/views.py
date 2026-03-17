import django.views.generic as generic_views
from django.contrib.auth.models import User
from django.urls import reverse_lazy
import django.contrib.auth.mixins as mixins
from django.utils.translation import gettext_lazy, gettext
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.users.forms import CustomUserCreationForm


class UserMixin:
    model = User
    login_url = reverse_lazy("login")


class OnlyOwnerMixin(
    mixins.LoginRequiredMixin,
    mixins.UserPassesTestMixin
):
    def test_func(self):
        return self.get_object() == self.request.user


class UserCreateView(
    UserMixin,
    generic_views.CreateView,
    ):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "task_manager/users/form.html"
    extra_context = {
        "header": gettext_lazy("Registration"),
        "submit_button_label": gettext_lazy("Sign up")
    }

    def form_valid(self, form):
        messages.success(
            self.request, gettext("User successfully registered")
        )
        return super().form_valid(form)


class UserListView(
    UserMixin,
    generic_views.ListView,
    ):
    template_name = "task_manager/users/list.html"


class UserUpdateView(
    UserMixin,
    OnlyOwnerMixin,
    generic_views.UpdateView,
):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")
    template_name = "task_manager/users/form.html"
    extra_context = {
        "header": gettext_lazy("Edit user"),
        "submit_button_label": gettext_lazy("Modify")
        }

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        messages.error(self.request, gettext("You cannot edit another user"))
        return redirect("users:list")

    def form_valid(self, form):
        messages.success(
            self.request, gettext("User successfully updated")
        )
        return super().form_valid(form)


class UserDeleteView(
    UserMixin,
    OnlyOwnerMixin,
    generic_views.DeleteView,
):
    success_url = reverse_lazy("index")
    template_name = "task_manager/users/delete.html"

    def form_valid(self, form):
        user = self.get_object()
        if user.tasks_authored.exists() or user.tasks_executing.exists():
            messages.error(
                self.request, gettext("Cannot delete a user linked to tasks")
            )
            return redirect("users:list")
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        messages.error(self.request, gettext("You cannot delete another user"))
        return redirect("users:list")
