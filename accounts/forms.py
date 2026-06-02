from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ConfirmEmailForm(forms.Form):
    code = forms.CharField(max_length=6)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class ResetConfirmForm(forms.Form):
    code = forms.CharField(max_length=6)
    new_password = forms.CharField(
        widget=forms.PasswordInput
    )