import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from Problems.forms import TaskForm
from Problems.models import Task


def tasks_list(request):
    all_tasks = Task.objects.all()

    context = {'all_tasks': all_tasks}
    return render(request, 'Problems/tasks_list.html', context)


def tasks_edit_task(request, task_id):

    task = Task.objects.get(id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task.body = form.cleaned_data['body']
            task.ans = form.cleaned_data['ans']
            task.source = form.cleaned_data['source']
            task.save()
            return redirect('tasks_read_task', task_id)

    task_form = TaskForm(initial={'body': task.body, 'ans': task.ans, 'source': task.source})
    context = {'task_form': task_form}
    return render(request, 'Problems/tasks_edit_task.html', context)



def tasks_read_task(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'Problems/tasks_read_task.html', context)


def tasks_create_task(request):

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.save()
            return redirect('tasks_list')

    task_form = TaskForm()
    context = {'task_form': task_form}
    return render(request, 'Problems/tasks_create_task.html', context)


def tasks_delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks_list')

    context = {'task': task}
    return render(request, 'Problems/tasks_delete_task.html', context)


def try_ajax(request):

    all_data = request.POST.get('all_data')
    all_data = json.loads(all_data)

    for cell in all_data:
        task_id = cell['task_id']
        task_field = cell['task_field']
        task_field_value = cell['field_value']

        task = Task.objects.get(id=task_id)

        if task_field == 'ans':
            task.ans = task_field_value
        elif task_field == 'body':
            task.body = task_field_value
        elif task_field == 'source':
            task.source = task_field_value

        task.save()

    return HttpResponse(str(task.id))


def tasks_list_edit_grid(request):
    all_tasks = Task.objects.all()

    context = {'all_tasks': all_tasks}
    return render(request, 'Problems/tasks_list_edit_grid.html', context)
