from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from django.contrib.auth.decorators import login_required

from .models import EmailConfirm,Profile
from .forms import (
    RegisterForm,
    LoginForm,
    ConfirmEmailForm,
    ForgotPasswordForm,
    ResetConfirmForm,
)


def send_confirmation_email(user):
    code = randint(100000, 999999)

    EmailConfirm.objects.update_or_create(
        user=user,
        defaults={'code': code}
    )

    send_mail(
        subject='Confirm your account',
        message=f'Hello {user.username}, your confirmation code: {code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )


def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        # Проверяем существует ли активный пользователь
        existing_user = User.objects.filter(username=username, is_active=True).first()
        if existing_user:
            return render(
                request,
                'accounts/register.html',
                {'form': form, 'error': 'Username already exists'}
            )

        # Удаляем неактивных пользователей с тем же username
        User.objects.filter(
            username=username,
            is_active=False
        ).delete()

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            user.is_active = False
            user.save()

            Profile.objects.get_or_create(
                user=user
            )

            send_confirmation_email(user)

    
            confirm = EmailConfirm.objects.filter(user=user).first()

            return render(
                request,
                'accounts/confirm_email.html',
                {
                    'username': user.username,
                    'confirmation_code': confirm.code if confirm else None
                }
            )
        except Exception as e:
            return render(
                request,
                'accounts/register.html',
                {'form': form, 'error': f'Error creating user: {str(e)}'}
            )

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            return redirect('home')
	
        inactive_user = User.objects.filter(
            username=username,
            is_active=False
        ).first()

        error = (
            'Confirm your email first'
            if inactive_user
            else 'Invalid username or password'
        )

        return render(
            request,
            'accounts/login.html',
            {
                'form': form,
                'error': error
            }
        )

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


def forgot_password(request):
    form = ForgotPasswordForm()

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            user = User.objects.filter(email=email).first()

            if not user:
                return render(request, 'accounts/forgot_password.html', {
                    'form': form,
                    'error': 'Email not found'
                })

            send_confirmation_email(user)

            return redirect('reset_confirm')

    return render(request, 'accounts/forgot_password.html', {
        'form': form
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def reset_confirm(request):
    form = ResetConfirmForm()

    if request.method == 'POST':
        form = ResetConfirmForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password']

            confirm = EmailConfirm.objects.filter(code=code).first()

            if not confirm:
                return render(request, 'accounts/reset_confirm.html', {
                    'form': form,
                    'error': 'Wrong code'
                })

            user = confirm.user
            user.set_password(new_password)
            user.save()

            confirm.delete()

            return redirect('login')

    return render(request, 'accounts/reset_confirm.html', {
        'form': form
    })


def confirm_email(request):
    form = ConfirmEmailForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = request.POST.get('username')
        code = form.cleaned_data['code']

        user = User.objects.filter(
            username=username
        ).first()

        if not user:
            return render(
                request,
                'accounts/confirm_email.html',
                {
                    'form': form,
                    'error': 'User not found'
                }
            )

        confirm = EmailConfirm.objects.filter(
            user=user,
            code=code
        ).first()

        if not confirm:
            return render(request,'accounts/confirm_email.html',{'form': form,'error': 'Invalid code'})

        user.is_active = True
        user.save()
        confirm.delete()

        # Автоматически логиним пользователя после подтверждения email
        from django.contrib.auth import login
        login(request, user)

        return redirect('home')

    return render(request,'accounts/confirm_email.html',{'form': form})



@login_required
def profile(request):
    return render(request,'accounts/profile.html',{'profile': request.user.profile})

from .forms import ProfileForm


@login_required
def profile_update(request):

    profile = request.user.profile

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if form.is_valid():
        form.save()
        return redirect('profile')

    return render(
        request,
        'accounts/profile_update.html',
        {
            'form': form
        }
    )
# Create your views here.
