from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task, Activity, Flight, Invitation
from django.views import View
import requests
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages


def HomePage(request):
    user_tasks = Task.objects.filter(user=request.user)
    invited_tasks = Invitation.objects.filter(receiver=request.user).values_list('task', flat=True)

    tasks = Task.objects.filter(Q(id__in=user_tasks) | Q(id__in=invited_tasks))

    return render(request, 'home.html', {'tasks': tasks})

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
            return redirect('signup')
    
    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('signup')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        date_range_str = request.POST.get('dateRange')

        task = Task(user=request.user, title=title, location=location, date_range=date_range_str)
        task.save()

    return redirect('home')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check if the user is the owner of the task
    if task.user != request.user:
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('home')

    task.delete()
    return redirect('home')

def hello_world(request):
    return render(request, 'hello_world.html')

def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    activities = Activity.objects.filter(task_id=task.id)

    if request.method == 'POST':
        flight_number = request.POST.get('flight_number')
        aviationstack_api_key = settings.AVIATIONSTACK_API_KEY
        api_url = f'http://api.aviationstack.com/v1/flights?access_key={aviationstack_api_key}&flight_iata={flight_number}'

        response = requests.get(api_url)
        data = response.json()

        if data['pagination']['total'] > 0:
            flight_data = data['data'][0]

            flight = Flight.objects.create(
                flight_number=flight_data['flight']['iata'],
                airline=flight_data['airline']['name'],
                departure_airport=flight_data['departure']['iata'],
                arrival_airport=flight_data['arrival']['iata']
            )

            return render(request, 'task_detail.html', {'task': task, 'activities': activities, 'flight': flight})
        else:
            error_message = 'Flight not found. Please enter a valid flight number.'
            return render(request, 'task_detail.html', {'task': task, 'activities': activities, 'error_message': error_message})

    activities = Activity.objects.filter(task_id=task.id)

    return render(request, 'task_detail.html', {'task': task, 'activities': activities})

def add_activity(request, task_id):
    if request.method == 'POST':
        Activity.objects.create(
            task_id=task_id,
            activity=request.POST.get('activity'),
            date=request.POST.get('date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time')
        )
    return redirect('task_detail', task_id=task_id)

def trip_options(request, task_id):
    trip_data = ... 

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return HttpResponse("Task not found", status=404)

    context = {'trip_data': trip_data, 'task': task}
    return render(request, 'trip_options.html', context)

def invite_user(request, task_id, username):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        invite_username = request.POST.get('inviteUsername')
        receiver_user = User.objects.filter(username=invite_username).first()

        invitation = Invitation(sender=request.user, receiver=receiver_user, task=task)
        invitation.save()

        messages.success(request, f'Invitation sent to {receiver_user.username}.')
        return redirect('home') 

    return render(request, 'home.html', {'task': task})

class ChatPageView(View):
    def get(self, request):
        return render(request, 'chat/chatPage.html')
    
