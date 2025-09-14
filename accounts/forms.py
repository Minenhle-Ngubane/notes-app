from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm, 
    UserChangeForm as DjangoUserChangeForm,
    AuthenticationForm as DjangoAuthenticationForm
)

from .models import User


class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
        })


class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text=_("Required. Enter a valid email address.")
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
        })

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    

class UserChangeForm(DjangoUserChangeForm):

    class Meta:
        model = User
        fields = ("email", "avatar", "first_name", "last_name",)
        
        widgets = {
            "avatar": forms.FileInput,
        }