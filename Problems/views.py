from django.shortcuts import render

# Create your views here.
from Problems.forms import TaskForm
from Problems.models import Task


def tasks(request):

    if request.method == 'POST':
        new_task = Task()
        new_task.body = request.POST.get('body')
        new_task.ans = request.POST.get('ans')
        new_task.source = request.POST.get('source')
        new_task.save()

    all_tasks = Task.objects.all()
    task_form = TaskForm()
    context = {'all_tasks': all_tasks, 'task_form': task_form}
    return render(request, 'Problems/tasks.html', context)