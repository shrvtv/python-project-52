from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=gettext_lazy("First name"))
    last_name = forms.CharField(label=gettext_lazy("Last name"))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = gettext_lazy("Username")
        self.fields["password1"].label = gettext_lazy("Password")
        self.fields["password2"].label = gettext_lazy("Password confirmation")
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["required"] = ""
            field.widget.attrs["placeholder"] = field.label


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = gettext_lazy("Username")
        self.fields["password"].label = gettext_lazy("Password")
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["required"] = ""
            field.widget.attrs["placeholder"] = field.label
