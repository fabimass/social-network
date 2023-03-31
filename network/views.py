from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Post
from .forms import NewPostForm
from .utils import addLikesInfo


def index(request): 

    return render(request, "network/index.html", {
        "newpost": NewPostForm(),
        "posts": addLikesInfo(Post.objects.all().order_by('-date_posted'), request.user)
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


def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            newpost = Post(
                content=form.cleaned_data["post"], 
                posted_by=request.user,
                date_posted=datetime.now())
            newpost.save()
            
    return HttpResponseRedirect(reverse("index"))


def likes(request, postid):
    post = Post.objects.get(id=postid)
    
    if request.method == "POST":
        # Toggle the like status
        if post.is_liked_by(request.user):
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)

    return(JsonResponse({
        "status": post.is_liked_by(request.user),
        "count": post.likes_count()}, 
        status=200))


def user_page(request, username): 
    
    return render(request, "network/user.html", {
        "username": username,
        "posts": addLikesInfo(User.objects.get(username=username).posts_made.all().order_by('-date_posted'), request.user) 
    })


def follow(request, username): 

    user = User.objects.get(username=username)

    if request.method == "POST":
        # Toggle the follow status
        if user.is_followed_by(request.user):
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
   
    return(JsonResponse({
        "following": user.following.all().count(),
        "followers": user.followers.all().count(),
        "currently_following": user.is_followed_by(request.user)}, 
        status=200))


def following(request): 

    posts = Post.objects.none()

    for user_followed in request.user.following.all():
        posts = posts | user_followed.posts_made.all()

    return render(request, "network/index.html", {
       
        "posts": addLikesInfo(posts.order_by('-date_posted'), request.user)
    })