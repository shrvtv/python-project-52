import django.views.generic as views
import django.contrib.auth.mixins as mixins


class StatusCreateView(
    mixins.LoginRequiredMixin,
    views.CreateView
):
    pass


class StatusDeleteView(
    mixins.LoginRequiredMixin,
    views.DeleteView
):
    pass


class StatusListView(
    mixins.LoginRequiredMixin,
    views.ListView
):
    pass


class StatusUpdateView(
    mixins.LoginRequiredMixin,
    views.UpdateView
):
    pass
