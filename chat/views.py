from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def chatPage(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login-user")
	context = {}
	return render(request, "task_list.html", context)

