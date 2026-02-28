from django import forms
from task_manager.tasks.models import Task
from django.utils.translation import gettext
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        empty_label="---------",
        label=gettext("Status")
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label="---------",
        label=gettext("Executor")
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=gettext("Labels")
    )
    self_tasks = forms.BooleanField(
        required=False,
        label=gettext("Only my tasks")
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "self_tasks":
                field.widget.attrs['class'] = "form-check-input mr-3"
            else:
                field.widget.attrs['class'] = "form-select ml-2 mr-3"


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selectors = ('status', 'executor', 'labels')
        mandatory = ('name', 'status')
        for name, field in self.fields.items():
            field.widget.attrs['class'] = (
                'form-select' if name in selectors else 'form-control'
            )
            if name in mandatory:
                field.widget.attrs['required'] = ''
            if name == 'description':
                field.widget.attrs['cols'] = '40'
                field.widget.attrs['rows'] = '10'
            if name == 'label':
                field.widget.attrs
            field.widget.attrs['placeholder'] = gettext(field.label)
