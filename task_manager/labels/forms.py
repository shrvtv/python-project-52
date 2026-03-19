from django import forms
from django.utils.translation import gettext, gettext_lazy

from task_manager.labels.models import Label


class LabelCreationForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('name',)
        labels = {
            'name': gettext_lazy('Name'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["required"] = ""
            field.widget.attrs['placeholder'] = gettext(field.label)
