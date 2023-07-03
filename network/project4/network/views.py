from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from itertools import chain
import json
from django.http import JsonResponse

from .models import User
from .models import Posts
from .models import Follow
from .models import Like

likedPosts = []
def index(request):
    currentUser = request.user
    likedPosts.clear()
    posts = Posts.objects.all().order_by('-date')
    likes = Like.objects.all()
    
    for like in likes:
        if like.user.id == currentUser.id:
            likedPosts.append(like.post.id)
    if posts.exists():
        return render(request, "network/index.html",{
            "posts":posts,
            "request":request,
            "likedposts":likedPosts
        })
    else:
        return render(request, "network/index.html",{
            "message":"There are no posts. Be the first !",
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
    
@login_required(login_url="/login")
def newpost(request):
    if request.method == "POST":
        user = request.user
        post = request.POST['post']

        postdata = Posts(
            username = user,
            post = post,
            likes = 0,
        )

        postdata.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request,name):
    profile_user = get_object_or_404(User, username = name)
    posts = Posts.objects.filter(username__username=profile_user).order_by('-date')
    likes = Like.objects.all()
    likedPosts.clear()
    currentUser = request.user
    isFollowing = False
    followers_count = profile_user.followers_count
    following_count = profile_user.following_count

    for like in likes:
        if like.user.id == currentUser.id:
            likedPosts.append(like.post.id)

    
    user_instance = Follow.objects.filter(user=currentUser).first()
    if user_instance:
        if user_instance.follows.filter(pk=profile_user.pk):
            isFollowing = True
        else:
            isFollowing = False

    return render(request,"network/profile.html",{
        "profile_user":profile_user,
        "posts":posts,
        "message":"This user has no posts",
        "isfollowing":isFollowing,
        "followers_count":followers_count,
        "following_count":following_count,
        "likedposts":likedPosts
    })


@login_required(login_url="/login")
def follow(request,id):
    currentUser = request.user
    follow = User.objects.get(pk=id)
    existing_user_instance = Follow.objects.filter(user=currentUser).first()
    if existing_user_instance:
        existing_user_instance.follows.add(follow)
        
    else:
        follow_instance = Follow.objects.create(user=currentUser)
        follow_instance.follows.set([follow])

    follow.followers_count = follow.followers_count + 1
    follow.save()
       
    currentUser.following_count = currentUser.following_count + 1
    currentUser.save()

    return HttpResponseRedirect(reverse("profile",args=(follow.username, )))

@login_required(login_url="/login")
def unfollow(request,id):
    currentUser = request.user
    unfollow = User.objects.get(pk=id)
    user_instance = Follow.objects.filter(user=currentUser).first()
    user_instance.follows.remove(unfollow)

    unfollow.followers_count = unfollow.followers_count - 1
    unfollow.save()

    currentUser.following_count = currentUser.following_count - 1
    currentUser.save()
    return HttpResponseRedirect(reverse("profile",args=(unfollow.username, )))

@login_required(login_url="/login")
def following(request):
    currentUser = request.user.id
    likedPosts.clear()
    following = Follow.objects.filter(user=currentUser)
    following_users_ids = list(chain.from_iterable([follow.follows.all() for follow in following]))
    following_posts = Posts.objects.filter(username__in=following_users_ids)
    likes = Like.objects.all()
    for like in likes:
        if like.user.id == currentUser:
            likedPosts.append(like.post.id)
    return render(request,"network/following.html",{
        'current_user':currentUser,
        'following':following_posts,
        'likedposts':likedPosts
    })



@login_required(login_url="/login")
def addlike(request,id):
    post = Posts.objects.get(pk=id)
    user = request.user
    newlike = Like(user=user,post=post)
    newlike.save()
    post.likes = post.likes + 1
    post.save()
    likedPosts.append(id)

    return JsonResponse({"message":"Like added"})

@login_required(login_url="/login")
def removelike(request,id):
    post = Posts.objects.get(pk=id)
    user = request.user
    like = Like.objects.filter(user=user,post=post)
    like.delete()
    post.likes = post.likes - 1
    post.save()
    if id in likedPosts:
        likedPosts.remove(id)
    return JsonResponse({"message":"Like removed"})

def getlikedposts(request):
    return JsonResponse({'likedposts':likedPosts})  






        
            

    

