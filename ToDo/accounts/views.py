from django.contrib.auth import authenticate, login
from .forms import RegisterForm, UserUpdateForm, SimplePasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from tasks.models import Task
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, "Неверный логин или пароль")
            return redirect('login')

    return render(request, 'auth/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) 

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user

    # статистика
    tasks = Task.objects.filter(user=user)

    total_tasks = tasks.count()
    done_tasks = tasks.filter(status='done').count()

    if total_tasks > 0:
        progress = int((done_tasks / total_tasks) * 100)
    else:
        progress = 0

    user_form = UserUpdateForm(instance=user)
    password_form = SimplePasswordChangeForm(user)

    if request.method == 'POST':

        if 'update_user' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=user)

            if user_form.is_valid():
                user_form.save()
                return redirect('profile')

        elif 'change_password' in request.POST:
            password_form = SimplePasswordChangeForm(user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Пароль успешно изменён")
                return redirect('profile')

    return render(request, 'auth/profile.html', {
        'user_form': user_form,
        'password_form': password_form,
        'total_tasks': total_tasks,
        'done_tasks': done_tasks,
        'progress': progress,
    })