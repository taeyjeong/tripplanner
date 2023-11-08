from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'tasks'
        
class Activity(models.Model):
    activity = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)  # Make 'task' nullable

    def __str__(self):
        return self.activity