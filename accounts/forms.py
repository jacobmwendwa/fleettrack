import re

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm
)
from django.contrib.auth.models import User


def validate_strong_password(password):
    if len(password) < 8:
        raise forms.ValidationError(
            'Password must be at least 8 characters long.'
        )

    if not re.search(r'[A-Z]', password):
        raise forms.ValidationError(
            'Password must contain at least one uppercase letter.'
        )

    if not re.search(r'[a-z]', password):
        raise forms.ValidationError(
            'Password must contain at least one lowercase letter.'
        )

    if not re.search(r'[0-9]', password):
        raise forms.ValidationError(
            'Password must contain at least one number.'
        )

    if not re.search(r'[^A-Za-z0-9]', password):
        raise forms.ValidationError(
            'Password must contain at least one symbol.'
        )

    return password


class StrongPasswordCreationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label='Email address'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        return validate_strong_password(password)


class StrongPasswordResetForm(SetPasswordForm):

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        return validate_strong_password(password)