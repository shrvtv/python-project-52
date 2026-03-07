from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy

import django.contrib.auth.views as auth_views
import django.views.generic as generic_views

from task_manager.users.forms import CustomAuthenticationForm

class IndexView(generic_views.TemplateView):
    template_name = "index.html"


class LoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy("index")
    template_name = "login.html"
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, gettext_lazy("You are logged in")
        )
        return response


class LogoutView(auth_views.LogoutView):
    http_method_names = ["post"]
    next_page = reverse_lazy("index")
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, gettext_lazy("You logged out")
        )
        return response
