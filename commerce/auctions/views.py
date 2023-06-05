from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Listings
from .models import Comments
from .models import Bids

from .forms import ListingForm

from decimal import Decimal


def index(request):

    listings = Listings.objects.all().filter(isactive = True).order_by('-created')
    if listings.exists():
        return render(request,"auctions/index.html",{
            "listings": listings,

        })
    else:
        return render(request,"auctions/index.html",{
            "message": "There are no active listings"
        })


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

@login_required(login_url="/login")
def newlisting(request):
    form = ListingForm(request.POST or None)
    if request.method == "GET":
        return render(request,"auctions/newlisting.html",{
            'form':form
        })
    else:
        submitbutton = request.POST.get("submit")
        title = ''
        description = ''
        category = ''
        price = ''
        if form.is_valid():
            title = form.cleaned_data['listing_title']
            description = form.cleaned_data['listing_description']
            category = form.cleaned_data['listing_category']
            price = form.cleaned_data['listing_price']
        newlisting = Listings(
            user_id = request.user,
            title = title,
            description = description,
            category = category,
            current_price = price,
            isactive = True
        )
        newlisting.save()
        return HttpResponseRedirect(reverse("index"))

def listing(request,id):
    listingDetails = Listings.objects.get(pk=id)
    currentUser = request.user
    isListingInWatchlist = False
    isSeller = False
    if listingDetails.user_id == currentUser:
        isSeller = True
    comments = Comments.objects.filter(listing_id = id)
    if currentUser in listingDetails.watchlist.all():
        isListingInWatchlist = True
    else:
        isListingInWatchlist = False
    return render(request,"auctions/listing.html",{
        "listing":listingDetails,
        "isListingInWatchList":isListingInWatchlist,
        "comments":comments,
        "isSeller":isSeller
    })

@login_required
def removeWatchList(request,id):
    listingDetails = Listings.objects.get(pk=id)
    currentUser = request.user
    listingDetails.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

@login_required
def addWatchList(request,id):
    listingDetails = Listings.objects.get(pk=id)
    currentUser = request.user
    listingDetails.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

@login_required
def watchlist(request):
    currentUser = request.user
    listings = Listings.objects.filter(watchlist=currentUser)
    if listings:
        return render(request,"auctions/watchlist.html",{
            "listings":listings
        })
    else:
        message = "There are no watchlisted items"
        return render(request,"auctions/watchlist.html",{
            "message":message
        })

def categories(request):
    categories = [choice[1] for choice in Listings.category_choices]
    return render(request,"auctions/categories.html",{
        "categories":categories
    })

def category(request,category):
    listings=Listings.objects.filter(category=category)
    if listings:
        return render(request,"auctions/category.html",{
            "listings":listings,
            "category":category
        })
    else:
        message = "There are no active listings in this category"
        return render(request,"auctions/category.html",{
            "message":message,
            "category":category
        })

@login_required   
def addcomment(request,id):
    currentUser = request.user
    listingDetails = Listings.objects.get(pk=id)
    comment = request.POST['newComment']

    newComment = Comments(
        user_id = currentUser,
        listing_id = listingDetails,
        comment = comment
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))

@login_required
def placebid(request,id):
    currentUser = request.user
    currentListing = Listings.objects.get(pk=id)
    currentPrice = currentListing.current_price
    bid = Decimal(request.POST['placebid'])
    isSeller = False

    if currentListing.user_id == currentUser:
        isSeller = True

    if bid > currentPrice and isSeller == False :
        newBid = Bids(
            user_id = currentUser,
            listing_id = currentListing,
            price = bid
        )
        newBid.save()
    
        currentListing.current_price = bid
        currentListing.last_bidder = currentUser
        currentListing.save()    

    return HttpResponseRedirect(reverse("listing",args=(id, )))

@login_required
def closeBids(request,id):
    currentListing = Listings.objects.get(pk=id)
    if currentListing.last_bidder:
        winner = currentListing.last_bidder
        currentListing.isactive = False
        currentListing.save()
    else:
        currentListing.isactive = False
        currentListing.save()
    return HttpResponseRedirect(reverse("index"))

def history(request):
    listings = Listings.objects.all().filter(isactive = False).order_by('created')
    if listings.exists():
        return render(request,"auctions/history.html",{
            "listings": listings,

        })
    else:
        return render(request,"auctions/index.html",{
            "message": "Nothing to show"
        })

@login_required
def mylistings(request):
    currentUser = request.user
    userListings = Listings.objects.all().filter(user_id=currentUser, isactive=True).order_by('-created')
    if userListings:
        return render(request,"auctions/mylistings.html",{
            "listings":userListings,
            "user":currentUser
        })
    else:
        message = "You don't have any active listings"
        return render(request,"auctions/mylistings.html",{
            "message":message,
            "user":currentUser
        })






