from django import forms
from django.utils.translation import gettext, gettext_lazy

from task_manager.tasks.models import Task


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
        labels = {
            'name': gettext_lazy('Name'),
            'description': gettext_lazy('Description'),
            'status': gettext_lazy('Status'),
            'executor': gettext_lazy('Executor'),
            'labels': gettext_lazy('Labels'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selectors = ('status', 'executor', 'labels')
        mandatory = ('name', 'status')
        self.fields["executor"].label_from_instance = (
            lambda user: user.get_full_name()
        )
        for name, field in self.fields.items():
            field.widget.attrs['class'] = (
                'form-select' if name in selectors else 'form-control'
            )
            if name in mandatory:
                field.widget.attrs['required'] = ''
            if name == 'description':
                field.widget.attrs['cols'] = '40'
                field.widget.attrs['rows'] = '10'
            field.widget.attrs['placeholder'] = gettext(field.label)
