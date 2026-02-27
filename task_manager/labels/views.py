import django.views.generic as views
import django.contrib.auth.mixins as mixins
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelCreationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy


app_label = "labels"


class LabelMixin(mixins.LoginRequiredMixin):
    model = Label
    login_url = reverse_lazy("login")
    def get_success_url(self):
        return reverse_lazy("labels:list")


class LabelCreateView(
    LabelMixin,
    views.CreateView,
):
    form_class = LabelCreationForm
    template_name = "task_manager/labels/form.html"
    extra_context = {
        "header": gettext_lazy("Create label"),
        "submit_button_label": gettext_lazy("Create")
    }


class LabelListView(
    LabelMixin,
    views.ListView,
):
    #template_name = "task_manager/labels/list.html"
    pass


class LabelUpdateView(
    LabelMixin,
    views.UpdateView,
):
    form_class = LabelCreationForm
    template_name = "task_manager/labels/form.html"
    extra_context = {
        "header": gettext_lazy("Edit label"),
        "submit_button_label": gettext_lazy("Edit")
    }


class LabelDeleteView(
    LabelMixin,
    views.DeleteView,
):
    #template_name = "task_manager/labels/delete.html"
    pass
