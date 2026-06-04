from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем встроенную валидацию username Django
        self.fields['username'].validators = []
        self.fields['username'].help_text = ''
        self.fields['username'].required = True
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        # Убираем строгие требования к паролю
        self.fields['password1'].validators = []
        self.fields['password1'].help_text = ''
        self.fields['password1'].required = True
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].validators = []
        self.fields['password2'].help_text = ''
        self.fields['password2'].required = True
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Проверяем только активных пользователей
        if User.objects.filter(username=username, is_active=True).exists():
            raise forms.ValidationError('Username already exists')
        return username

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


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio','avatar']