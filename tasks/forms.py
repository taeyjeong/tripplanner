# flight_tracker/forms.py

from django import forms

class FlightForm(forms.Form):
    flight_number = forms.CharField(label='Enter Flight Number', max_length=10)
