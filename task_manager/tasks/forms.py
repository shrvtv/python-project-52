from django import forms
from task_manager.tasks.models import Task
from django.utils.translation import gettext


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selectors = ('status', 'executor')
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
            field.widget.attrs['placeholder'] = gettext(field.label)
