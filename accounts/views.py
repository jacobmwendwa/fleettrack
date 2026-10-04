from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy

from .models import Task
from .forms import (
    StrongPasswordCreationForm,
    StrongPasswordResetForm,
)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = StrongPasswordCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = StrongPasswordCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()

        if title:
            Task.objects.create(
                user=request.user,
                title=title
            )

        return redirect('dashboard')

    tasks = Task.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'accounts/dashboard.html',
        {'tasks': tasks}
    )


@login_required
@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect('dashboard')


@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.delete()

    return redirect('dashboard')


@login_required
def profile_view(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(
        request,
        'accounts/profile.html',
        context
    )


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        user.save()

        return redirect('profile')

    context = {
        'user': user,
    }

    return render(
        request,
        'accounts/edit_profile.html',
        context
    )


class FleetPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class FleetPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class FleetPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = StrongPasswordResetForm
    success_url = reverse_lazy('password_reset_complete')


class FleetPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'