import django.forms as forms
import django_filters as filters
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = []

    status = filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        empty_label="---------",
        label=gettext_lazy("Status"),
    )
    executor = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="---------",
        label=gettext_lazy("Executor"),
    )
    labels = filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
        label=gettext_lazy("Labels"),
    )
    self_tasks = filters.BooleanFilter(
        label=gettext_lazy("Only my tasks"),
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(executor=self.request.user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["executor"].label_from_instance = (
            lambda user: user.get_full_name()
        )
        for name, field in self.form.fields.items():
            if name == "self_tasks":
                field.widget.attrs['class'] = "form-check-input mr-3"
            else:
                field.widget.attrs['class'] = "form-select ml-2 mr-3"
