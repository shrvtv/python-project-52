from django.shortcuts import render
import django.contrib.auth.views as auth_views
import django.views.generic as generic_views


class IndexView(generic_views.TemplateView):
    template_name = "index.html"


class LoginView(auth_views.LoginView):
    pass


class LogoutView(auth_views.LogoutView):
    http_method_names = ["post"]
    pass
