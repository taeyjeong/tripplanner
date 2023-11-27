from django.shortcuts import redirect, render
from .models import Task, Activity, Flight
from django.http import HttpResponse

from django.conf import settings
from .forms import FlightForm
import requests



# Create your views here.

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

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
    return render(request, 'task_detail.html', {'task': task})

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


def flight_tracker(request):
    form = FlightForm()

    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            flight_number = form.cleaned_data['flight_number']
            aviationstack_api_key = settings.AVIATIONSTACK_API_KEY
            api_url = f'http://api.aviationstack.com/v1/flights?access_key={aviationstack_api_key}&flight_iata={flight_number}'

            response = requests.get(api_url)
            data = response.json()

            if data['pagination']['total'] > 0:
                flight_data = data['data'][0]

                # Save flight information to the database
                flight = Flight.objects.create(
                    flight_number=flight_data['flight']['iata'],
                    airline=flight_data['airline']['name'],
                    departure_airport=flight_data['departure']['iata'],
                    arrival_airport=flight_data['arrival']['iata']
                )

                return render(request, 'task_detail.html', {'flight': flight})
            else:
                error_message = 'Flight not found. Please enter a valid flight number.'
                return render(request, 'task_detail.html', {'form': form, 'error_message': error_message})

    return render(request, 'task_detail.html', {'form': form})
