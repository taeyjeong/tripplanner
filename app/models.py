from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True, blank=True)  
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

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
