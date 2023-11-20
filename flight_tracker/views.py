from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import FlightForm
from .models import Flight

# Create your views here.
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

                return render(request, 'flight_tracker/flight_details.html', {'flight': flight})
            else:
                error_message = 'Flight not found. Please enter a valid flight number.'
                return render(request, 'flight_tracker/flight_tracker.html', {'form': form, 'error_message': error_message})

    return render(request, 'flight_tracker/flight_tracker.html', {'form': form})
