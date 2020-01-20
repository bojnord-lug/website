from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import Log_in, Sign_in
from .models import Post, Profile, Event, Category, Comment, EventImage

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
import json
from datetime import datetime


@csrf_exempt
def index(request):
    all_Posts = list(Post.objects.order_by("-date").all()[:3])
    three_events = list(Event.objects.order_by("-date").all()[:3])
    all_events = list(Event.objects.order_by("-date").all()[3:])
    event_images = EventImage.objects.all()[:9]
    page_obj = Paginator(all_events, 3)
    if request.method == 'POST':
        page = page_obj.page(int(request.body.decode()))
        return HttpResponse(render(request, 'ajax.html', {"page_obj": page.object_list, "num_pages": range(page_obj.num_pages)}))
    page = page_obj.page(1)
    most_recent_categories =  sorted([i for i in Category.objects.all()], 
                                        key=lambda x: x.post_set.count())[::-1][:5]

<<<<<<< HEAD
    return render(request, 'index.html', {"Posts": all_Posts, "events": three_events, "all_events": all_events, "page_obj": page.object_list, "num_pages": range(page_obj.num_pages), 'recent_categories': most_recent_categories})
=======
    return render(request, 'index.html', {"event_images": event_images, "Posts": all_Posts, "events": three_events, "all_events": all_events, "page_obj": page.object_list, "num_pages": range(page_obj.num_pages)})
>>>>>>> 2a83085f6d631662f32bd123d23730355b2a1480


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'login.htm')


def profile(request):
    return render(request, "profile.html")


def contact(request):
    return render(request, "contact.html")


def category(request):
    latest_Posts = list(Post.objects.order_by("-date").all()[:3])
    categoryName = Category.objects.get(pk=request.GET.get("id"))
    all_Posts = list(Post.objects.order_by(
        "-date").filter(category=request.GET.get("id")))
    event_images = EventImage.objects.all()[:9]

    page_obj = Paginator(all_Posts, 3)
    if request.method == 'POST':
        page = page_obj.page(int(request.body.decode()))
        return HttpResponse(render(request, 'ajax.html', {"page_obj": page.object_list, "num_pages": range(page_obj.num_pages)}))
    page = page_obj.page(1)

    most_recent_categories =  sorted([i for i in Category.objects.all()], 
                                        key=lambda x: x.post_set.count())[::-1][:5]

    return render(request, 'category.html', {"event_images": event_images, "categoryName": categoryName, "latest_Posts": latest_Posts, "all_Posts": all_Posts, "page_obj": page.object_list, "num_pages": range(page_obj.num_pages), 'recent_categories': most_recent_categories})


def single(request):
    latest_Posts = list(Post.objects.order_by("-date").all()[:3])
    post = Post.objects.get(pk=request.GET.get("id"))
    author_Posts = list(Post.objects.order_by(
        "-date").filter(author=post.author.id)[:2])
    event_images = EventImage.objects.all()[:9]
    comments = list(Comment.objects.order_by(
        "-date").filter(post=post.id))
    date_format = "%Y-%m-%d"
    for item in comments:
        a = datetime.strptime(str(datetime.now().date()), date_format)
        b = datetime.strptime(str(item.date), date_format)
        delta = b - a
        item.date = abs(delta.days)

    most_recent_categories =  sorted([i for i in Category.objects.all()], 
                                        key=lambda x: x.post_set.count())[::-1][:5]

    return render(request, "single.html", {"event_images": event_images, "comments": comments, "author_Posts": author_Posts, "post": post, "tags": tags, "latest_Posts": latest_Posts, 'recent_categories': most_recent_categories, 'categories': post.category.all()})


@require_POST
@csrf_exempt
def Signin(request):
    u = request.POST.get('name')
    e = request.POST.get('email')
    p = request.POST.get('passwd')
    person = authenticate(request, username=u, password=p)
    if person is not None:
        return render(request, "sign_in.html", {"error": "this accont is already ."})
    elif u == "" or e == "" or p == "":
        return render(request, "sign_in.html", {"error": "Please complate the form"})
    else:
        user = User.objects.create_user(u, e, p)
        user.save()
        login(request, user)
        request.session["user"] = u
        return HttpResponseRedirect("/")


@require_POST
@csrf_exempt
def Login(request):
    form = Log_in(request.POST)
    if form.is_valid():
        name = form.cleaned_data.get("username")
        paswd = form.cleaned_data.get("passwd")
        user = authenticate(request, username=name, password=paswd)
        if user is not None and not request.user.is_authenthicated:
            login(request, user)
            request.session["user"] = name
            return redirect("/")
        elif request.user.is_authenthicated:
            return redirect("/")
    else:
        return render(request, "login_form.html", {"error": "please complate the form corectly ..."})
