from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

from .models import *


@login_required(login_url="login")
def index(request, category=None):
    auctions = Auction.objects.raw(
        "SELECT * FROM auctions_auction AS a JOIN auctions_bids AS b ON a.id = b.auction_id_id WHERE a.status = 'open'"
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
        price = request.POST["price"]
        try:
            image = request.FILES["image"]
        except:
            image = None

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
            return render(
                request,
                "auctions/error.html",
                {
                    "error": 400,
                    "error_message": f"Your bid does not fall within the established parameters. Do not use commas for values ​and separate the decimal with a period",
                },
            )
        if (
            bid >= current_bid.starting_bid
            and (current_bid.current_bid is None or bid > current_bid.current_bid)
            and current_bid.user_id != request.user
            and request.user != auction_search.user_id
        ):
            current_bid.current_bid = bid
            current_bid.user_id = request.user
            current_bid.bidders_quantity += 1
            current_bid.save()
        else:
            return render(
                request,
                "auctions/error.html",
                {
                    "error": 400,
                    "error_message": f"Your bid does not fall within the established parameters. You can't bid on a listing that is yours or you are winning and your bid must not be lower than the last bid",
                },
            )
        return HttpResponseRedirect(reverse("listing", args=[auction]))
    else:
        if current_bid.current_bid:
            bid = current_bid.current_bid
        else:
            bid = current_bid.starting_bid
        try:
            watchlists = auction_search.auction_favorite.filter(
                user_id=request.user
            ).get()
        except:
            watchlists = None
        return render(
            request,
            "auctions/listing.html",
            {
                "watchlists": watchlists,
                "auction": auction_search,
                "bids": current_bid,
                "current_bid": round(bid, 2),
                "comments": Comments.objects.filter(auction_id=auction),
            },
        )


@login_required(login_url="login")
def categories(request):
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": Auction.objects.values("category").distinct(),
        },
    )


@login_required(login_url="login")
def category_list(request, category):
    auctions = Auction.objects.filter(category=category)
    return render(
        request,
        "auctions/selected.html",
        {
            "auction_listing": auctions,
            "category": category,
        },
    )


@login_required(login_url="login")
def watchlist(request):
    list_wacth = Watchlist.objects.filter(user_id=request.user).select_related(
        "auction_id"
    )
    return render(
        request,
        "auctions/selected.html",
        {
            "auction_listing": list_wacth,
        },
    )


@login_required(login_url="login")
def change_watchlist(request, auction_id):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")

        if action == "takeout":
            try:
                watch_auction = (
                    Watchlist.objects.filter(auction_id=auction_id)
                    .filter(user_id=request.user)
                    .get()
                )
            except:
                return render(
                    request,
                    "auctions/error.html",
                    {"error": 400, "error_message": "Error deleting from watchlist"},
                )
            else:
                watch_auction.delete()
        elif action == "put":
            auction = Auction.objects.get(pk=auction_id)
            new_watch = Watchlist(auction_id=auction, user_id=request.user)
            new_watch.save()

        return JsonResponse({"message": "Success"})
