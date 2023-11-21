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
        
        liked_posts = set(request.user.likes.filter(like=True).values_list('post_id', flat=True))
        for post in posts:
            post.is_liked = post.id in liked_posts
        return render(request, "network/index.html", {
            "posts": posts
        })
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def change_follow(request, user_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    user = User.objects.get(pk=user_id)
    data = json.loads(request.body).get("follow")

    if data == "True":
        if Follow.objects.filter(user=request.user, following=user_id).exists():
            follow = Follow.objects.get(user=request.user, following=user)
            follow.delete()
            return JsonResponse({"message": "Follow was removed succesfully", "status": 1}, status=201, safe=False)
        else:
            return JsonResponse({"error": "Data not found"}, status=500, safe=False)
    elif data == "False":
        if not Follow.objects.filter(user=request.user, following=user_id).exists():
            follow = Follow(user=request.user, following=user)
            follow.save()
            return JsonResponse({"message": "Follow was added succesfully", "status": 1}, status=201, safe=False)
        else:
            return JsonResponse({"error": "Data already exists"}, status=500, safe=False)



@csrf_exempt
@login_required
def like(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=request.user.id)
        if Likes.objects.filter(user=user, post=post).exists():
            like = Likes.objects.get(user=user, post=post)
            if like.like == True:
                like.like = False
                like.save()
                post.likes_post -= 1
                post.save()
                return JsonResponse({"message": "Like was removed succesfully", "likes": post.likes_post}, status=201, safe=False)
            else:
                like.like = True
                like.save()
                post.likes_post += 1
                post.save()
                return JsonResponse({"message": "Like was added succesfully", "likes": post.likes_post}, status=201, safe=False)
        else:
            like = Likes(user=user, post=post, like=True)
            like.save()
            post.likes_post += 1
            post.save()
            return JsonResponse({"message": "Like was added succesfully", "likes": post.likes_post}, status=201, safe=False)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
    
@login_required
def following(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        posts = Post.objects.filter(user__in=user.following.values('id')).order_by("-timestamp").all()
        liked_posts = set(request.user.likes.filter(like=True).values_list('post_id', flat=True))
        for post in posts:
            post.is_liked = post.id in liked_posts
        return render(request, "network/follow.html", {
            "posts": posts
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    
@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user_id).order_by("-timestamp").all()
    followers = Follow.objects.filter(following=user_id).count()
    following = Follow.objects.filter(user=user_id).count()
    liked_posts = set(request.user.likes.filter(like=True).values_list('post_id', flat=True))
    for post in posts:
        post.is_liked = post.id in liked_posts
    if request.user.is_authenticated:
        if request.user == user_id:
            return render(request, "network/profile.html", {
                "user_id": user,
                "posts": posts,
                "followers": followers,
                "following": following
            })
        else:
            following_list = set(request.user.following.filter(following=user_id))
            if following_list:
                follow = True
            else:
                follow = False
            return render(request, "network/profile.html", {
                "user_id": user,
                "posts": posts,
                "followers": followers,
                "following": following,
                "follow": follow
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


