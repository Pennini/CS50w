from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Group, Area, Position, Event, Project, Meeting, Availabilty

# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request, "system/index.html")

@login_required(login_url="login")
def profile(request):
    return render(request, "system/profile.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            user = User.objects.get(email=email)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        except User.DoesNotExist:
            return render(request, "system/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "system/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

