from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *


def index(request):

    return render(request, "auctions/index.html", {
        "listings" : Auctions.objects.filter(active=True)
    })

def listing_nologin(request, id):
    listing = Auctions.objects.get(pk=id)

    return render(request, "auctions/notloggedin.html", {
        "listing" : listing,
        "comments" : Comments.objects.filter(auction=id)
    })

@login_required
def create_listing(request):

    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories" : Categories.objects.all()
        })

    cat = request.POST["category"]
    print(cat)

    NewListing = Auctions(
        title = request.POST["title"],
        description = request.POST["description"],
        price = float(request.POST["price"]),
        photo = request.POST["photo"],
        category = Categories.objects.get(category=cat),
        seller = request.user,
    )

    NewListing.save()
    return index(request)


@login_required
def listing(request, id):

    listing = Auctions.objects.get(pk=id)
    bids = Bids.objects.filter(auction=id)
    highestbid = Bids.objects.filter(auction=id).order_by("-amount").first()

    if listing.active == False:
        if request.user == highestbid.bidder:
            return render(request, "auctions/bought.html", {
                "listing" : listing,
                "bids" : bids,
            })

    watchlistitem = Watchlist.objects.filter(auction=id, user=request.user)

    return render(request, "auctions/listing.html", {
        "listing" : listing,
        # "user" : user,
        "bids" : bids,
        "comments" : Comments.objects.filter(auction=id),
        "watchlist": Watchlist.objects.filter(auction=id),
        "user": request.user,
        "watchlistitem" : watchlistitem
    })


@login_required
def bidorclose(request, id):

    auction = Auctions.objects.get(pk=id)

    if request.user == auction.seller:
        if request.method == "POST":
            auction.active = False
            auction.save()
    else:
        if request.method == "POST":
            bid = request.POST["bid"]
            if float(bid) > auction.price:
                NewBid = Bids(
                    amount = float(bid),
                    bidder = request.user
                )
                NewBid.save()
                auction.price = float(bid)
                auction.save()
                print(auction)

    return listing(request, id)

@login_required
def comment(request, id):

    if request.method == "POST":
        NewComment = Comments(
            post = request.POST["comment"],
            user = request.user,
            auction = Auctions.objects.get(pk=id)
        )
        NewComment.save()

    return listing(request, id)

@login_required
def watchlist(request, id):

    watchlistitem = Watchlist.objects.filter(auction=id, user=request.user)

    if request.method == "POST":
        if watchlistitem:
            watchlistitem.delete()
        else:
            NewWatchlist = Watchlist(
                auction = Auctions.objects.get(pk=id),
                user = request.user
            )
            NewWatchlist.save()

    return listing(request, id)

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
