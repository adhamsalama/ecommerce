from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import User, ListItem, Comment, Bid, WatchlistItem
from .forms import ListItemForm, CommentForm


def index(request):
    items = ListItem.objects.filter(open=True).order_by("-date")
    return render(request, "auctions/index.html", {"items": items})



def item_page(request, item_id):
    try:
        item = ListItem.objects.get(pk=item_id)
    except ListItem.DoesNotExist:
        return render(request, "auctions/error.html", {"message": "Item does not exist"})
    #comments = Comment.objects.filter(item=item)
    comments = item.comments.all().order_by("-date")
    #bids = Bid.objects.filter(item=item).order_by("-date")
    bids = item.bids.all()
    if bids:
        bids = bids.order_by("-date")
    user_bids = []
    for bid in bids:
        if bid.user == request.user:
            user_bids.append(bid)
    comment_form = CommentForm()
    return render(request, "auctions/item_page.html", {"item": item, "comments": comments,
                    "bids": bids, "user_bids": user_bids,  "comment_form": comment_form})


@require_http_methods(["POST"])
def bid(request):
    bid_value = float(request.POST["bid_value"])
    item_id = request.POST["item_id"]
    item = ListItem.objects.get(pk=item_id)
    bids = item.bids.all().order_by("-value")
    if not bids: # no bids yet
        if bid_value <= item.price:
            return render(request, "auctions/error.html", {"message": "Your bid is too low"})
    else:
        highest_bid = bids[0]
        if bid_value <= highest_bid.value:
            return render(request, "auctions/error.html", {"message": "Your bid is too low"})
    bid_ = Bid(value=bid_value, item=item, user=request.user)
    bid_.save()
    return HttpResponseRedirect(reverse("item_page", kwargs={"item_id": item_id}))


@require_http_methods(["POST"])
def close_auction(request):
    item_id = request.POST["item_id"]
    item = ListItem.objects.get(pk=item_id)
    item.open = False
    item.save()
    return HttpResponseRedirect(reverse("item_page", kwargs={"item_id": item_id}))


def create_listing(request):
    form = ListItemForm()
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {"form": form})
    else:
        form = ListItemForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.owner = request.user
            new_item.highest_bid = new_item.price
            new_item.save()
        return HttpResponseRedirect(reverse("item_page", kwargs={"item_id": new_item.id}))

@require_http_methods(["POST"])
def comment(request):
    comment = Comment()
    comment.user = request.user
    comment.item = ListItem.objects.get(pk=request.POST["item_id"])
    comment.text = request.POST["text"]
    comment.save()
    return HttpResponseRedirect(reverse("item_page", kwargs={"item_id": request.POST["item_id"]}))
    

@require_http_methods(["GET"])
def category(request, category_name):
    items = ListItem.objects.filter(category=category_name, open=True)
    return render(request, "auctions/category.html", {"items": items})


@require_http_methods(["GET"])
def categories(request):
    categories_ = ListItem.objects.all().values("category").distinct().order_by("-category")
    return render(request, "auctions/categories.html", {"categories": categories_})


@require_http_methods(["POST"])
def add_to_watchlist(request):
    item = ListItem.objects.get(pk=request.POST["item_id"])
    watchlist_item = WatchlistItem(item=item, user=request.user)
    watchlist_items = request.user.watchlist.all()
    for i in watchlist_items:
        if i.item == item:
            messages.info(request, 'Item already in your Watchlist.')
            return HttpResponseRedirect(reverse("watchlist"))
    watchlist_item.save()
    messages.success(request, "Item added to your Watchlist.")
    return HttpResponseRedirect(reverse("watchlist"))


@require_http_methods(["POST"])
def delete_from_watchlist(request):
    item = ListItem.objects.get(pk=request.POST["item_id"])
    request.user.watchlist.get(item=item).delete()
    messages.success(request, "Item deleted from your Watchlist.")
    return HttpResponseRedirect(reverse("watchlist"))



@require_http_methods(["GET"])
def watchlist(request):
    watchlist_items = request.user.watchlist.all().order_by("-date")
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist_items})












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
