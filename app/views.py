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

def WelcomePage(request):
    if request.method == 'POST':
        button_clicked = request.POST.get('button_clicked', '')

        if button_clicked == 'create_account':
            return redirect('signup')  # Redirect to the signup page

        elif button_clicked == 'sign_in':
            return redirect('login')  # Redirect to the login page

    return render(request, 'welcome.html')

def HomePage(request):
    user_tasks = Task.objects.filter(user=request.user)
    invited_tasks = Invitation.objects.filter(receiver=request.user).values_list('task', flat=True)

    tasks = Task.objects.filter(Q(id__in=user_tasks) | Q(id__in=invited_tasks))

    context = {
        'tasks': tasks,
        'user_tasks': user_tasks,
        'invited_tasks': invited_tasks,
    }

    return render(request, 'home.html', context)

def SignupPage(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        phone_number = request.POST.get('phoneNumber')
        email = request.POST.get('email')

        # Store user information in the session
        request.session['user_info'] = {
            'email': email,
            'first_name': first_name,
            'phone_number' : phone_number
        }

        # Redirect to set_password view
        return redirect('set_password')

    return render(request, 'signup.html')

def setPassword(request):
    if request.method == 'POST':
        # Retrieve user information from the session
        user_info = request.session.get('user_info', None)

        if user_info:
            email = user_info.get('email', '')
            first_name = user_info.get('first_name', '')
            phone_number = user_info.get('phone_number', '')
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')

            if password != password2:
                error_message = "Passwords do not match."
                return render(request, 'set_password.html', {'error_message': error_message})

            if not User.objects.filter(email=email).exists():
                # Create a new user
                user = User.objects.create_user(username=first_name, email=email, password=password)
                user.first_name = first_name
                user.save()

                # Log in the user (optional)
                login(request, user)

                # Clear user information from the session
                request.session.pop('user_info', None)

                # Redirect to the set_password view
                return redirect('login')
            else:
                # Handle the case when the user already exists
                error_message = "User with this email already exists."
                return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'set_password.html')


def LoginPage(request):
    if request.method == 'POST':
        user_input = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=user_input, password=password)
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
 # Get tasks owned by the user
    user_tasks = Task.objects.filter(user=request.user)

    # Get tasks invited to the user
    invited_tasks = Task.objects.filter(invited_users=request.user)

    return render(request, 'task_list.html', {'user_tasks': user_tasks, 'invited_tasks': invited_tasks})

        
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
    # Assuming you have some logic here to retrieve or calculate trip_data
    trip_data = ...  # Your logic to get or calculate trip_data

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

        if receiver_user is None:
            messages.error(request, 'User not found with the given username.')
            return redirect('home') 

        if receiver_user == request.user:
            messages.error(request, 'You cannot invite yourself to your own task.')
            return redirect('home') 

        invitation = Invitation(sender=request.user, receiver=receiver_user, task=task)
        invitation.save()

        messages.success(request, f'Invitation sent to {receiver_user.username}.')
        return redirect('home') 

    return render(request, 'home.html', {'task': task})

class ChatPageView(View):
    def get(self, request):
        return render(request, 'chat/chatPage.html')
    
