from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from calendar import Calendar, month_name
import datetime as dt

from .models import User, Group, Area, Position, Event, Project, Meeting, Availabilty

# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request, "system/index.html")

@login_required(login_url="login")
def profile(request):
    return render(request, "system/profile.html")

@login_required(login_url="login")
def availability(request):
    HOUR_CHOICES = [(f"{i}:00", f"{i + 1}:00") for i in range(9, 21)]
    return render(request, "system/availability.html", {
        "hour_choices": HOUR_CHOICES
    })

@login_required(login_url="login")
def calendar(request):
    month = dt.datetime.now().month
    year = dt.datetime.now().year
    cal = Calendar().monthdayscalendar(year, month)

    return render(request, "system/calendar.html", {
        "calendar": cal,
        "month": month_name[month],
        "year": year
    })

@login_required(login_url="login")
def create_view(request, intention):
    if request.user.is_staff and intention in ["user", "event", "project"]:
        return render(request, "system/create.html", {
            "intention": intention
        })
    else:
        return render(request, "system/create.html", {
            "message": intention
        })


@login_required(login_url="login")
def create(request, intention):
    return HttpResponseRedirect(reverse('create_view', args=[intention]))


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            return render(request, "system/login.html", {
                "message": "Invalid email and/or password."
            })
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "system/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "system/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

