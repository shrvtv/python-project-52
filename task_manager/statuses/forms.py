from django import forms
from task_manager.statuses.models import Status
from django.utils.translation import gettext


class StatusCreationForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''
            field.widget.attrs['placeholder'] = gettext(field.label)
