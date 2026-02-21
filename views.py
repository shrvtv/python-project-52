from django.shortcuts import render
from django.urls import reverse_lazy

import django.contrib.auth.views as auth_views
import django.views.generic as generic_views


class IndexView(generic_views.TemplateView):
    template_name = "index.html"


class LoginView(auth_views.LoginView):
    next_page = reverse_lazy("index")


class LogoutView(auth_views.LogoutView):
    http_method_names = ["post"]
    next_page = reverse_lazy("index")
