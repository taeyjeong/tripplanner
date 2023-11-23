from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task, Activity


# Create your views here.
@login_required
def HomePage(request):
    return render(request, 'task_list.html')

def SignupPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("Your passwords dont match.")
        else:
            my_user= User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect('login')
        
    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Username or Password is incorrect')
    
    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if not title or not date or not start_time or not end_time:
            return HttpResponse("Please fill in all required fields.")

        # Create a new task with the provided data
        task = Task(user=request.user, title=title, date=date, start_time=start_time, end_time=end_time)
        task.save()

    return redirect('task_list')

def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
    return redirect('task_list')

def hello_world(request):
    return render(request, 'hello_world.html')

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

    return render(request, 'task_detail.html', {'task': task, 'activities': activities})
