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


            



        

    
