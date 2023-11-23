from django.urls import path
from . import views

urlpatterns = [
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('task_list/', views.task_list, name='task_list'),  # Updated path
    path('create/', views.create_task, name='create_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('hello-world/', views.hello_world, name='hello_world'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]
