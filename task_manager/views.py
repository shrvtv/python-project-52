from django.urls import reverse_lazy

import django.contrib.auth.views as auth_views
import django.views.generic as generic_views

from task_manager.users.forms import CustomAuthenticationForm

class IndexView(generic_views.TemplateView):
    template_name = "index.html"


class LoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy("index")
    template_name = "login.html"


class LogoutView(auth_views.LogoutView):
    http_method_names = ["post"]
    next_page = reverse_lazy("index")
