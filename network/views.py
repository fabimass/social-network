from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from datetime import datetime
import json

from .models import User, Post
from .forms import NewPostForm
from .utils import addLikesInfo


def index(request): 
    objects = Post.objects.all().order_by('-date_posted')
    pages = Paginator(objects, 10)
    current_page = int(request.GET.get("page", 1))

    return render(request, "network/index.html", {
        "newpost": NewPostForm(),
        "posts": addLikesInfo(pages.page(current_page).object_list, request.user),
        "pages": range(1, pages.num_pages+1),
        "current_page": current_page,
        "prev_page": current_page-1,
        "next_page": current_page+1,
        "last_page": pages.num_pages
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


def single_post(request, postid):
    post = Post.objects.get(id=postid)
    
    if request.method == "PUT":
        new_content = json.loads(request.body)["content"]
        post.content = new_content
        post.save()

    return(JsonResponse({
        "content": post.content,
        "poster": post.posted_by.username}, 
        status=200))


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

    objects = User.objects.get(username=username).posts_made.all().order_by('-date_posted')
    pages = Paginator(objects, 10)
    current_page = int(request.GET.get("page", 1))
    
    return render(request, "network/user.html", {
        "username": username,
        "posts": addLikesInfo(pages.page(current_page).object_list, request.user),
        "pages": range(1, pages.num_pages+1),
        "current_page": current_page,
        "prev_page": current_page-1,
        "next_page": current_page+1,
        "last_page": pages.num_pages 
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

    objects = posts.order_by('-date_posted')
    pages = Paginator(objects, 10)
    current_page = int(request.GET.get("page", 1))

    return render(request, "network/index.html", {
        "posts": addLikesInfo(pages.page(current_page).object_list, request.user),
        "pages": range(1, pages.num_pages+1),
        "current_page": current_page,
        "prev_page": current_page-1,
        "next_page": current_page+1,
        "last_page": pages.num_pages
    })