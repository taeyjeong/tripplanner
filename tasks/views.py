# views.py

from django.shortcuts import render, redirect
from django.conf import settings
from .models import Task, Activity, Flight
import requests

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST.get('title'),
            date=request.POST.get('date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time')
        )
    return redirect('task_list')

def delete_task(request, task_id):
    if request.method == 'POST':
        Task.objects.filter(id=task_id).delete()
    return redirect('task_list')

def hello_world(request):
    if request.method == 'POST':
        return redirect('task_list')
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