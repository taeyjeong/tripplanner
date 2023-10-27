from django.shortcuts import redirect, render
from .models import Task

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

def hello_world(request):
    return render(request, 'tasks/hello_world.html')