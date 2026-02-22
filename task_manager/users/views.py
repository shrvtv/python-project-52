import django.views.generic as generic_views


class UserListView(generic_views.ListView):
    pass


class UserCreateView(generic_views.CreateView):
    pass


class UserUpdateView(generic_views.UpdateView):
    pass


class UserDeleteView(generic_views.DeleteView):
    pass
