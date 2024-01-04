from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task, Activity, Flight
from django.views import View
import requests
from django.conf import settings
from datetime import datetime


def HomePage(request):
    tasks = Task.objects.all()  # Fetch all tasks from the database
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


def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

        
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        date_range_str = request.POST.get('dateRange')

        task = Task(user=request.user, title=title, location=location, date_range=date_range_str)
        task.save()

    return redirect('home')


def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
    return redirect('home')

def hello_world(request):
    return render(request, 'hello_world.html')

def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        # Handle the case where the task does not exist
        return HttpResponse("Task not found", status=404)

    activities = Activity.objects.filter(task_id=task.id).order_by('date', 'start_time')

    if request.method == 'POST':
        flight_number = request.POST.get('flight_number')
        aviationstack_api_key = settings.AVIATIONSTACK_API_KEY
        api_url = f'http://api.aviationstack.com/v1/flights?access_key={aviationstack_api_key}&flight_iata={flight_number}'

        response = requests.get(api_url)
        data = response.json()

        if data['pagination']['total'] > 0:
            flight_data = data['data'][0]

            # Create and save Flight object
            flight = Flight.objects.create(
                flight_number=flight_data['flight']['iata'],
                airline=flight_data['airline']['name'],
                departure_airport=flight_data['departure']['iata'],
                arrival_airport=flight_data['arrival']['iata']
            )

            # Create and save Activity object for tracking the flight
            Activity.objects.create(
                task_id=task.id,
                activity=f"Tracked Flight {flight.flight_number}",
                date=flight_data['departure']['estimated'].split('T')[0],  # Extract YYYY-MM-DD
                start_time=flight_data['departure']['estimated'].split('T')[1],  # Extract HH:MM:SS
                end_time=flight_data['arrival']['estimated'].split('T')[1]  # Extract HH:MM:SS
            )


            return render(request, 'task_detail.html', {'task': task, 'activities': activities, 'flight': flight})
        else:
            error_message = 'Flight not found. Please enter a valid flight number.'
            return render(request, 'task_detail.html', {'task': task, 'activities': activities, 'error_message': error_message})

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

    # Redirect to task_detail after adding activity and use task_id in the URL
    return redirect('task_detail', task_id=task_id)

def trip_options(request, task_id):
    trip_data = ...  # Your logic to get or calculate trip_data

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return HttpResponse("Task not found", status=404)

    context = {'trip_data': trip_data, 'task': task}
    return render(request, 'trip_options.html', context)

class ChatPageView(View):
    def get(self, request):
        return render(request, 'chat/chatPage.html')
    
