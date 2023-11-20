from django.urls import path
from flight_tracker import views

urlpatterns = [
    path('', views.flight_tracker, name='flight_tracker')   
]
