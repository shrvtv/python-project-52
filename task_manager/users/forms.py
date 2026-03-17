from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy, gettext
from django import forms


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["required"] = ""
            field.widget.attrs["placeholder"] = field.label


class CustomUserCreationForm(StyleMixin, UserCreationForm):
    first_name = forms.CharField(label=gettext_lazy("First name"))
    last_name = forms.CharField(label=gettext_lazy("Last name"))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


class CustomUserUpdateForm(StyleMixin, CustomUserCreationForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        qs = User.objects.exclude(pk=self.instance.pk)
        if qs.filter(username=username).exists():
            raise forms.ValidationError(
                gettext("A user with that username already exists.")
            )
        return username


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = gettext_lazy("Username")
        self.fields["password"].label = gettext_lazy("Password")
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["required"] = ""
            field.widget.attrs["placeholder"] = field.label
