import django.views.generic as generic


class TaskListView(generic.ListView):
    pass


class TaskCreateView(generic.CreateView):
    pass


class TaskUpdateView(generic.UpdateView):
    pass


class TaskDeleteView(generic.DeleteView):
    pass
