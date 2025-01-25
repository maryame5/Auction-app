from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *

from .models import *
from decimal import Decimal

def index(request):
    return render(request, "auctions/index.html" ,{
        "list_listings": listings.objects.all(),
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

@login_required
def create_listing(request):
    
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = Decimal(request.POST["price"])

        image_option = request.POST["image_option"]
        
        if image_option == "upload":
            image_url = request.FILES["image"]

        elif image_option == "url":
            image_url = request.POST["image_url"]
            
        cate=request.POST["category"]
    
        categor = category.objects.get(id=cate)
        


        listing = listings.objects.create(title=title, description=description,
                 image=image_url, bid=bid, category=categor, user=request.user)
        

        # Create a bids instance and assign it to the listings instance
        bid = bids.objects.create(price=bid, user=request.user, listings=listing)
       
    
        return redirect('index')
    else:
    
        return render(request, "auctions/create_listing.html",{
            "categories": category.objects.all()
        })
    


@login_required
def add_watchlist(request)   :
    if request.method == "POST":
            listing_id = request.POST.get('listing_id')
            listin = listings.objects.get(id=listing_id)
            try:
                 watchlist_entry = watchlist.objects.get(user=request.user, listing=listin)
            except watchlist.DoesNotExist:
    
                watchlist_entry = watchlist.objects.create(user=request.user, listing=listin)
            watchlist_entry.save()           
            
            return HttpResponseRedirect(reverse("index"))
@login_required
def remove_watchlist(request)   :
    if request.method == "POST":
            listing_id = request.POST.get('listing_id')
            listin = listings.objects.get(id=listing_id)
            watchlis = watchlist.objects.filter(user=request.user,listing=listin)
            watchlis.delete()
            return HttpResponseRedirect(reverse("index"))


@login_required
def view_watchlist(request):
    try:
        watchlis = watchlist.objects.filter(user=request.user)
        listing = [entry.listing for entry in watchlis]
     
    except watchlist.DoesNotExist:
        listing= []
    return render(request, "auctions/watchlist.html", {
        "listings": listing
    })
@login_required
def add_bid(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing = listings.objects.get(id=listing_id)
        older_bid = listing.bid
        bid = Decimal(request.POST["price"])
        if bid > older_bid:
            listing.bid = bid
            listing.save()
            bid=bids.objects.create(user=request.user,
            listings=listing,
            price=bid)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("view_listing", args=(listing.id,),)+ "?message=The new bid must be larger than the older one" )

def view_listing(request,listing_id):
    listing =listings.objects.get(id=listing_id)
    bid=listing.bid
    wonner = bids.objects.get(listings=listing,price=bid)
    
    #show tho te position of the user with a message
    if listing.is_close==True:
        if request.user== wonner.user:          
            message="you are the winner of this auction"
        elif request.user==listing.user:
            message="you are the owner of this auction, and you are closed this auction"
        else:
            message="this auction is closed"
    else:
        message=""
    #show comments in this listing
    list_com= comments.objects.filter(listing=listing)
    comment=[entry.comment for entry in list_com]
     # show if the listing in the watchlist to show remove from watchlist or not
    watchlis = watchlist.objects.filter(user=request.user)
    listing_in_watch = [entry.listing for entry in watchlis]
    image = listing.image if 'http' in listing.image.url else listing.image.url
    return render(request, "auctions/listing.html",
                  {
                 "listing": listing,
                 "list_com": list_com,
                  "comment": comment,
                  "message_win":message,
                  "listing_in_watch":listing_in_watch,
                  "image":image
                  
                   })

  
@login_required
def comment(request):
    if request.method == "POST":
         listing_id = request.POST.get('listing_id')
         listing = listings.objects.get(id=listing_id)
         comment = comments.objects.create(
            user=request.user,
            listing=listing,
            comment=request.POST["comment"]
            )
         comment.save()
         return HttpResponseRedirect(reverse("view_listing", args=(listing.id,)))
    


def categories(request):
        return render(request, "auctions/categories.html",{
        "list_category": category.objects.all(),  
    })
def categor(request,categor):
    list_category=category.objects.get(name=categor)
    list_listings=listings.objects.filter(category=list_category)
    return render(request, "auctions/category.html",{
        "list_listings":list_listings,
        "category":categor})


'''everything above working don't touch it'''    
@login_required
def close_auction(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing = listings.objects.get(id=listing_id)
    
        user=request.user
        create_user=listing.user
        if user == create_user:
            listing.is_close=True
            listing.save()
            
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def won(request):
    listing_id = request.POST.get('listing_id')
    listing = listings.objects.get(id=listing_id)
    bid=listing.bid
    wonner = bids.objects.get(listings=listing,price=bid)
    print(wonner.user)
    if request.user== wonner.user:
        if listing.is_close==True:
            return HttpResponseRedirect(reverse("view_listing", args=(listing.id,),)+ "?message=CONGRAT  YOU ARE THE WINNING OF THIS AUCTIONS" )
        

    return HttpResponseRedirect(reverse("view_listing", args=(listing.id,),)+ "?message= YOU ARE ""not"" THE WINNIr OF THIS AUCTIONS" )





   

        

