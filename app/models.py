from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    # Your existing fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # Add the date_range field
    date_range = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'registration'

class Activity(models.Model):
    activity = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.activity
    
    class Meta:
        app_label = 'registration'

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    departure_airport = models.CharField(max_length=50)
    arrival_airport = models.CharField(max_length=50)

    class Meta:
        app_label = 'registration'