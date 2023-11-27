from django.urls import path, include
from . import views, admin

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('hello-world/', views.hello_world, name='hello_world'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task_detailr/', views.flight_tracker, name='flight_tracker'),
]