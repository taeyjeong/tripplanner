# tasks/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Task, Activity, Flight
import requests

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        task = Task(title=title, date=date, start_time=start_time, end_time=end_time)
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
    activities = Activity.objects.filter(task_id=task.id)

    form = request.POST.get('flight_number')

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
            return render(request, 'task_detail.html', {'task': task, 'activities': activities, 'form': form, 'error_message': error_message})

    return render(request, 'task_detail.html', {'task': task, 'activities': activities, 'form': form})

def flight_tracker(request, task_id):
    task = Task.objects.get(id=task_id)
    activities = Activity.objects.filter(task_id=task.id)
    form = FlightForm(request.POST or None)

    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            flight_number = form.cleaned_data.get('flight_number')
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
                return render(request, 'task_detail.html', {'task': task, 'activities': activities, 'form': form, 'error_message': error_message})

    return render(request, 'task_detail.html', {'task': task, 'activities': activities, 'form': form})
