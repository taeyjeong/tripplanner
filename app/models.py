from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date_range = models.CharField(max_length=20, blank=True, null=True)
    invited_users = models.ManyToManyField(User, related_name='invited_tasks', blank=True)

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

class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} invites {self.receiver.username} to task '{self.task.title}'"

    class Meta:
        app_label = 'registration'