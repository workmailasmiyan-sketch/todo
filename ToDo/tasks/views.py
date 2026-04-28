from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Case, When, IntegerField
from .models import Task



@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    # ФИЛЬТР ПО СТАТУСУ
    status = request.GET.get('status')

    if status == 'todo':
        tasks = tasks.filter(status='todo')
    elif status == 'done':
        tasks = tasks.filter(status='done')

    # СОРТИРОВКА
    sort = request.GET.get('sort')

    if sort == 'priority':
        tasks = tasks.annotate(
            priority_order=Case(
                When(priority='high', then=1),
                When(priority='medium', then=2),
                When(priority='low', then=3),
                output_field=IntegerField()
            )
        ).order_by('priority_order')

    elif sort == 'deadline':
        tasks = tasks.order_by('deadline')

    else:
        tasks = tasks.order_by('-created_at')

    return render(request, 'tasks/list.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        deadline = request.POST.get('deadline')

        task = Task(
            title=title,
            description=description,
            priority=priority,
            status=status,
            user=request.user
        )

        # ДЕДЛАЙН
        if deadline:
            task.deadline = deadline

        task.save()

        return redirect('task_list')

    return render(request, 'tasks/create.html')


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':

        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')

        deadline = request.POST.get('deadline')

        # ДЕДЛАЙН
        if deadline:
            task.deadline = deadline
        else:
            task.deadline = None

        task.save()

        return redirect('task_list')

    return render(request, 'tasks/update.html', {'task': task})


@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')


@login_required
@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if task.status == 'todo':
        task.status = 'done'
    else:
        task.status = 'todo'

    task.save()

    return redirect('task_list')

