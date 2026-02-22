import django.views.generic as generic_views
from django.contrib.auth.models import User


class UserListView(generic_views.ListView):
    model = User
    queryset = User.objects.all()
    template_name = "task_manager/users/list.html"


class UserCreateView(generic_views.CreateView):
    pass


class UserUpdateView(generic_views.UpdateView):
    pass


class UserDeleteView(generic_views.DeleteView):
    pass
