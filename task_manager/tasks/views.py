import django.views.generic as generic


class TaskListView(generic.ListView):
    pass


class TaskDetailView(generic.DetailView):
    pass


class TaskCreateView(generic.CreateView):
    pass


class TaskUpdateView(generic.UpdateView):
    pass


class TaskDeleteView(generic.DeleteView):
    pass
