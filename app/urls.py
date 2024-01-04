from django.urls import path
from . import views

urlpatterns = [
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),
    path('home/home2', views.HomePage, name='home2'),
    path('logout/', views.LogoutPage, name='logout'),
    path('signup/', views.SignupPage, name='signup'),
    path('task_list/', views.task_list, name='task_list'), 
    path('create/', views.create_task, name='create_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('home/chat-page', views.ChatPageView.as_view(), name='chat-page'),
    path('add_activity/<int:task_id>/', views.add_activity, name='add_activity'),
    path('trip_options/<int:task_id>/', views.trip_options, name='trip_options'),
    path('invite_user/<int:task_id>/<str:username>/', views.invite_user, name='invite_user'),
]
