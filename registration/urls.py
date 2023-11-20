�
    N;<eC  �                   �|   � d Z ddlmZ ddlmZmZ  edej        j        �  �         ed ed�  �        �  �        gZdS )a  
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
�    )�admin)�path�includezadmin/� z
tasks.urlsN)	�__doc__�django.contribr   �django.urlsr   r   �site�urls�urlpatterns� �    �8C:\Users\Home\Documents\TAE\tripplanner\todolist\urls.py�<module>r      st   ��� �" !�  �  �  �  �  � %� %� %� %� %� %� %� %� 	�D��5�:�?�#�#��D��W�W�\�"�"�#�#����r   