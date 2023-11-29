from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
from calendar import Calendar, month_name
import datetime as dt
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

from .models import User, Group, Area, Position, Event, Project, Meeting, Availabilty

# Create your views here.
@login_required(login_url="login")
def index(request):
    projects = Project.objects.all().order_by("-start_day")
    events = Event.objects.all().order_by("-start_day")

    return render(request, "system/index.html", {
        "projects": projects,
        "events": events
    })

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

    projects = Project.objects.filter(start_day__month=month, start_day__year=year).order_by("start_day")
    events = Event.objects.filter(start_day__month=month, start_day__year=year).order_by("start_day")

    event_dict = {}
    for event in events:
        day_str = str(event.start_day.day)
        if day_str not in event_dict:
            event_dict[day_str] = [event]
        else:
            event_dict[day_str].append(event)

    project_dict = {}
    for project in projects:
        day_str = str(project.start_day.day)
        if day_str not in project_dict:
            project_dict[day_str] = [project]
        else:
            project_dict[day_str].append(project)
    print(event_dict)
    print(project_dict)

    return render(request, "system/calendar.html", {
        "calendar": cal,
        "month": month_name[month],
        "year": year,
        "event_dict": event_dict,
        "project_dict": project_dict
    })

@login_required(login_url="login")
def create_view(request, intention):
    if request.user.is_staff:
        if intention == "user":
            groups = Group.objects.all()
            areas = Area.objects.all()
            positions = Position.objects.all()
            return render(request, "system/create.html", {
                "intention": intention,
                "groups": groups,
                "areas": areas,
                "positions": positions
            })
        elif intention == "event":
            areas = Area.objects.all()
            members = User.objects.all()
            return render(request, "system/create.html", {
                "intention": intention,
                "areas": areas,
                "members": members
            })
        elif intention == "project":
            groups = Group.objects.all()
            members = User.objects.all()
            return render(request, "system/create.html", {
                "intention": intention,
                "groups": groups,
                "members": members
            })
        else:
            return render(request, "system/create.html", {
            "message": intention
        })
    else:
        return render(request, "system/create.html", {
            "message": intention
        })


@login_required(login_url="login")
def create(request, intention):
    if request.method == "POST":
        if intention == "user":
            username = request.POST["username"]
            is_staff = request.POST.get("staff", False)
            email = request.POST["email"]
            group = request.POST["group"]
            area = request.POST["area"]
            position = request.POST["position"]
            
            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]

            if not username or not email or not group or not area or not position:
                error_message = "Please fill all the fields."
            elif password != confirmation:
                error_message = "Passwords do not match."
            else:
                error_message = None

            groups = Group.objects.all()
            areas = Area.objects.all()
            positions = Position.objects.all()
            members = User.objects.all()

            if error_message:
                return render(request, "system/create.html", {
                    "message_error": error_message,
                    "intention": intention,
                    "groups": groups,
                    "areas": areas,
                    "positions": positions,
                    "members": members
                })
            
            if is_staff:
                is_staff = True
            
            group = Group.objects.get(pk=group)
            area = Area.objects.get(pk=area)
            position = Position.objects.get(pk=position)

            try:
                user = User.objects.create_user(username=username, email=email, password=password, is_staff=is_staff, group=group, area=area, position=position)
                user.save()
            except IntegrityError:
                groups = Group.objects.all()
                areas = Area.objects.all()
                positions = Position.objects.all()
                members = User.objects.all()
                return render(request, "system/create.html", {
                    "message_error": "Username already taken.",
                    "intention": intention,
                    "groups": groups,
                    "areas": areas,
                    "positions": positions,
                    "members": members
                })

            return render(request, "system/create.html", {
                    "message_error": "User created successfully.",
                    "intention": intention,
                    "groups": groups,
                    "areas": areas,
                    "positions": positions,
                    "members": members
                })
        
        elif intention == "project":
            name = request.POST["name"]
            description = request.POST["description"]
            group = request.POST["group"]
            category = request.POST["category"]
            start_date = request.POST["start-date"]
            start_time = request.POST["start-time"]
            end_date = request.POST["end-date"]
            end_time = request.POST["end-time"]
            members_project = request.POST.getlist("members")

            if not name or not description or not group or not start_date or not start_time or not members_project:
                error_message = "Please fill all the required fields. Including at least one member."
            elif end_date:
                if start_date > end_date:
                    error_message = "The ending date must be after the starting date."
                elif start_date == end_date and (start_time > end_time or start_time == end_time):
                    error_message = "The ending time must be after the starting time."
                else:
                    end_date_time = dt.datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
                    error_message = None
            elif not end_date and end_time:
                error_message = "Please fill the ending date."
            else:
                error_message = None
            
            groups = Group.objects.all()
            members = User.objects.all()

            if error_message:
                return render(request, "system/create.html", {
                    "message_error": error_message,
                    "intention": intention,
                    "groups": groups,
                    "members": members
                })
            
            start_date_time = dt.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            group = Group.objects.get(pk=group)
            
            project = Project.objects.create(name=name, responsible=request.user, description=description, group=group, start_day=start_date_time)
            if category:
                project.category = category
            if end_date:
                project.end_day = end_date_time
            project.members.set(members_project)

            project.save()

            return render(request, "system/create.html", {
                "message_error": "Project created successfully.",
                "intention": intention,
                "groups": groups,
                "members": members
            })
        
        elif intention == "event":
            name = request.POST["name"]
            description = request.POST["description"]
            area = request.POST["area"]
            category = request.POST["category"]
            start_date = request.POST["start-date"]
            start_time = request.POST["start-time"]
            end_date = request.POST["end-date"]
            end_time = request.POST["end-time"]
            members_event = request.POST.getlist("members")

            if not name or not description or not area or not start_date or not start_time or not members_event:
                error_message = "Please fill all the required fields. Including at least one member."
            elif end_date:
                if start_date > end_date:
                    error_message = "The ending date must be after the starting date."
                elif start_date == end_date and (start_time > end_time or start_time == end_time):
                    error_message = "The ending time must be after the starting time."
                else:
                    end_date_time = dt.datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
                    error_message = None
            elif not end_date and end_time:
                error_message = "Please fill the ending date."
            else:
                error_message = None
                

            areas = Area.objects.all()
            members = User.objects.all()

            if error_message:
                return render(request, "system/create.html", {
                    "message_error": error_message,
                    "intention": intention,
                    "areas": areas,
                    "members": members
                })
            
            start_date_time = dt.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            area = Area.objects.get(pk=area)
            
            event = Event.objects.create(name=name, responsible=request.user, description=description, area=area, start_day=start_date_time)
            if category:
                event.category = category
            if end_date:
                event.end_day = end_date_time

            event.members_planned.set(members_event)
            event.save()

            return render(request, "system/create.html", {
                    "message_error": "Event created successfully.",
                    "intention": intention,
                    "areas": areas,
                    "members": members
                })
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

