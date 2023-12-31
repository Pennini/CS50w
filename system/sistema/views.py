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
def meeting(request):
    position_list = ["director", "leader", "vice-president", "president"]
    if str(request.user.position) not in position_list:
        return render(request, "system/meeting.html", {
            "message": "You are not allowed to access this page."
        })
    else:
        groups = list(Group.objects.all())
        areas = list(Area.objects.all())
        return render(request, "system/meeting.html", {
            "group_list": groups,
            "area_list": areas,
        })
    
@csrf_exempt
@login_required(login_url="login")
def meeting_finish(request):
    if request.method == "POST":
        type_info = request.POST.get('type')
        id = request.POST.get('id')
        duration = request.POST.get('duration')
        members = request.POST.get('members').split(',')
        report = request.FILES.get('report')

        members = [User.objects.get(pk=int(member)) for member in members]
        
        if request.user not in members:
            members.append(request.user)

        meeting = Meeting.objects.create(duration=duration)
        
        if members != ['']:
            meeting.members_present.set(members)

        if type_info == 'group':
            group = Group.objects.get(pk=id)
            meeting.group = group
        elif type_info == 'area':
            area = Area.objects.get(pk=id)
            meeting.area = area
        else:
            return JsonResponse({"message": "Invalid type."})
        
        if report:
            meeting.report = report

        meeting.save()
        return JsonResponse({"message": "You have finished the meeting."})
    else:
        return JsonResponse({"message": "Invalid method."})

@csrf_exempt
@login_required(login_url="login")
def meeting_members(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("id")
        type = data.get("type")
        if type == "group":
            group = User.objects.filter(group=id)
            members = {member.username: member.id for member in group}
            return JsonResponse({"members": json.dumps(members)})
        elif type == "area":
            area = User.objects.filter(area=id)
            members = {member.username: member.id for member in area}
            return JsonResponse({"members": json.dumps(members)})
        else:
            return JsonResponse({"message": "Invalid type."})
    else:
        return JsonResponse({"message": "Invalid method."})

@login_required(login_url="login")
def search(request):
    search = request.GET.get("q")
    if search:
        projects = Project.objects.filter(name__icontains=search).order_by("-start_day")
        events = Event.objects.filter(name__icontains=search).order_by("-start_day")
        users = User.objects.filter(username__icontains=search)
        return render(request, "system/search.html", {
            "projects": projects,
            "events": events,
            "users": users
        })
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url="login")
def profile(request):
    projects_present = Project.objects.filter(members=request.user).count()
    events_present = Event.objects.filter(members_present=request.user).count()
    meetings_present = Meeting.objects.filter(members_present=request.user).count()

    score = projects_present + events_present + meetings_present

    return render(request, "system/profile.html", {
        "score": score
    })

@csrf_exempt
@login_required(login_url="login")
def display(request, id, type_info):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text")
        typeinfo = data.get("type")

        if not text or text == "":
            return JsonResponse({"message": "Text cannot be empty."})
        
        if typeinfo == "project":
            project = Project.objects.get(pk=id)
            project.description = text
            project.save()
            return JsonResponse({"message": "You have updated the description of this project."})
        elif typeinfo == "event":
            event = Event.objects.get(pk=id)
            event.description = text
            event.save()
            return JsonResponse({"message": "You have updated the description of this event."})
        else:
            return JsonResponse({"message": "Invalid type."})
    if type_info == "project":
        project = Project.objects.get(pk=id)
        return render(request, "system/display.html", {
            "info": project,
            "type": "project"
        })
    elif type_info == "event":
        event = Event.objects.get(pk=id)
        return render(request, "system/display.html", {
            "info": event,
            "type": "event"
        })
    else:
        return render(request, "system/display.html", {
            "message": "Couldn't find this data."
        })
    
@csrf_exempt
@login_required(login_url="login")
def bio(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text")
        
        if text == "":
            return JsonResponse({"message": "Bio cannot be empty."})
        
        if text:
            user = User.objects.get(pk=request.user.id)
            user.biography = text
            user.save()
        else:
            return JsonResponse({"message": "Bio cannot be empty."})

        return JsonResponse({"message": "Bio saved."})
    return render(request, "system/profile.html")

@csrf_exempt
@login_required(login_url="login")
def availability(request):
    HOUR_CHOICES = [(dt.time(i).strftime('%H:%M'), dt.time(i + 1).strftime('%H:%M')) for i in range(9, 21)]
    ava = Availabilty.objects.filter(user=request.user).order_by("day", "start_time")

    HOUR_DICT = {}
    for hour in HOUR_CHOICES:
        HOUR_DICT[(hour[0], hour[1])] = {day: status for day, status in ava.filter(start_time=hour[0]).values_list("day", "status")}
        
    if request.method == "POST":
        data = json.loads(request.body)
        day = data.get("day")
        start = data.get("start")
        end = data.get("end")


        if not day or not start or not end:
            return JsonResponse({"message": "Please fill all the fields."})
        
        try:
            day = int(day)
        except ValueError:
            return JsonResponse({"message": "Invalid date."})
        
        try:
            start = dt.datetime.strptime(start, "%H:%M").strftime("%H:%M")
        except ValueError:
            return JsonResponse({"message": "Invalid start time."})
        
        try:
            end = dt.datetime.strptime(end, "%H:%M").strftime("%H:%M")
        except ValueError:
            return JsonResponse({"message": "Invalid end time."})
        
        if start >= end:
            return JsonResponse({"message": "The ending time must be after the starting time."})
        
        if Availabilty.objects.filter(user=request.user, day=day, start_time=start, end_time=end).exists():
            availability = Availabilty.objects.get(user=request.user, day=day, start_time=start, end_time=end)
            availability.status = 0 if availability.status == 2 else availability.status + 1
            availability.save()
            return JsonResponse({"message": "You succesfully updated availability for this day.", "status": availability.status})
        else:
            availability = Availabilty.objects.create(user=request.user, day=day, start_time=start, end_time=end)
            availability.status = 0
            availability.save()
            return JsonResponse({"message": "Availability saved.", "status": availability.status})
    else:
        return render(request, "system/availability.html", {
            "hour_choices": HOUR_DICT
        })

@login_required(login_url="login")
def calendar(request):
    month = dt.datetime.now().month
    year = dt.datetime.now().year
    cal = Calendar().monthdays2calendar(year, month)

    projects = Project.objects.filter(start_day__month=month, start_day__year=year).order_by("start_day")
    events = Event.objects.filter(start_day__month=month, start_day__year=year).order_by("start_day")
    areas = Area.objects.all().order_by("meeting_day")
    groups = Group.objects.all().order_by("meeting_day")

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
    
    area_dict = {}
    for area in areas:
        day_str = str(area.meeting_day)
        if day_str not in area_dict:
            area_dict[day_str] = [area]
        else:
            area_dict[day_str].append(area)
    
    group_dict = {}
    for group in groups:
        day_str = str(group.meeting_day)
        if day_str not in group_dict:
            group_dict[day_str] = [group]
        else:
            group_dict[day_str].append(group)

    all_dict = {
        "events": event_dict,
        "projects": project_dict,
        "areas": area_dict,
        "groups": group_dict
    }

    return render(request, "system/calendar.html", {
        "calendar": cal,
        "month": month_name[month],
        "year": year,
        "all_dict": all_dict,
        "group_dict": group_dict,
        "area_dict": area_dict,
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

