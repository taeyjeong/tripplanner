from django.shortcuts import redirect, render
from .models import Task, Activity
from django.http import HttpResponse


# Create your views here.

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Create a new task with the provided data
        task = Task(title=title, date=date, start_time=start_time, end_time=end_time)
        task.save()

    return redirect('task_list')

def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
    return redirect('task_list')

def task_detail(request, task_id):
    task = Task.objects.get(pk=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

def hello_world(request):
    return render(request, 'tasks/hello_world.html')


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == 'POST':
        activity_name = request.POST.get('activity')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        activity = Activity(activity=activity_name, date=date, start_time=start_time, end_time=end_time, task=task)
        activity.save()

    activities = Activity.objects.filter(task_id=task.id)  # Use 'task_id' field to filter activities

    return render(request, 'tasks/task_detail.html', {'task': task, 'activities': activities})
