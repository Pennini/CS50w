from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .models import *


@login_required(login_url="login")
def index(request):
    auctions = Auction.objects.raw(
        "SELECT * FROM auctions_auction AS a JOIN auctions_bids AS b ON a.id = b.auction_id_id"
    )
    return render(request, "auctions/index.html", {"auction_listing": auctions})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


@login_required(login_url="login")
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def create_auction(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        image = request.FILES["image"]
        price = request.POST["price"]

        if not title or not description or not price:
            return render(
                request,
                "auctions/error.html",
                {
                    "error": 400,
                    "error_message": "Must provide title and description and the starting bid",
                },
            )
        else:
            auction = Auction(
                title=title, description=description, user_id=request.user
            )

            if image:
                auction.image = image
            if category:
                auction.category = category

            auction.save()
            price = Bids(auction_id=auction, starting_bid=price)
            price.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html")


@login_required(login_url="login")
def listing(request, auction):
    try:
        auction_search = Auction.objects.get(pk=auction)
        current_bid = Bids.objects.filter(auction_id=auction).get()
    except:
        return render(
            request,
            "auctions/error.html",
            {"error": 404, "error_message": f"The listing {auction} wasn't found."},
        )
    if request.method == "POST":
        try:
            bid = float(request.POST["bid"].replace(",", "."))
        except:
            return render(request, "auctions/error.html", {
                "error": 400,
                "error_message": f"Your bid does not fall within the established parameters. Do not use commas for values ​and separate the decimal with a period"
            })
        if bid >= current_bid.starting_bid and (current_bid.current_bid is None or bid > current_bid.current_bid) and current_bid.user_id != request.user and request.user != auction_search.user_id:
            current_bid.current_bid = bid
            current_bid.user_id = request.user
            current_bid.bidders_quantity += 1
            current_bid.save()
        else:
            return render(request, "auctions/error.html", {
                "error": 400,
                "error_message": f"Your bid does not fall within the established parameters. You can't bid on a listing that is yours or you are winning and your bid must not be lower than the last bid"
            })
        return HttpResponseRedirect(reverse('listing', args=[auction])) 
    else:
        if current_bid.current_bid:
            bid = current_bid.current_bid
        else:
            bid = current_bid.starting_bid
        return render(
            request,
            "auctions/listing.html",
            {
                "auction": auction_search,
                "bids": current_bid,
                "current_bid": round(bid, 2),
                "comments": Comments.objects.filter(auction_id=auction),
            },
        )
