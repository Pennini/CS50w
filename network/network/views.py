from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Likes, Follow


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.order_by("-timestamp").all()

        return render(request, "network/index.html", {
            "posts": posts
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    
@login_required
def profile(request, user_id):
    posts = Post.objects.filter(user=user_id).order_by("-timestamp").all()
    followers = Follow.objects.filter(following=user_id).count()
    following = Follow.objects.filter(user=user_id).count()
    if request.user.is_authenticated:
        if request.user == user_id:
            return render(request, "network/profile.html", {
                "posts": posts,
                "followers": followers,
                "following": following
            })
        else:
            return render(request, "network/profile.html", {
                "posts": posts,
                "followers": followers,
                "following": following,
                "follow": True
            })
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def compose(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    text = data.get("text")
    if not text:
        return JsonResponse({"error": "POST must have content"}, status=400)
    
    post = Post(user=request.user, content=text)
    post.save()

    return JsonResponse({"message": "POST was sent succesfully"}, status=201, safe=False)




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


