# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('task_list/', views.task_list, name='task_list'),
    
    path('create/', views.create_task, name='create_task'),
    path('create_task_and_show_hello_world/', views.create_task_and_show_hello_world, name='create_task_and_show_hello_world'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    
    path('task_detail/<int:task_id>/', views.task_detail, name='task_detail'),
    
    path('add_activity/<int:task_id>/', views.add_activity, name='add_activity'),
    path('trip_details/<int:task_id>/', views.trip_details, name='trip_details'),

]