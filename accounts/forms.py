from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем встроенную валидацию username Django
        self.fields['username'].validators = []
        self.fields['username'].help_text = ''
        # Убираем строгие требования к паролю
        self.fields['password1'].validators = []
        self.fields['password1'].help_text = ''
        self.fields['password2'].validators = []
        self.fields['password2'].help_text = ''

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
    
# accounts/forms.py

from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio','avatar']