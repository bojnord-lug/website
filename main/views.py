from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, Http404, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import LoginForm, SubmitComment, UpdateProfileForm
from .models import Post, Profile, Event, Category, Comment, EventImage, NewsLetter
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime

# hit_count = HitCount.objects.get_for_object(Post)


@csrf_exempt
def index(request):
    all_Posts = list(Post.objects.order_by("-date").all()[:3])
    all_events = list(Event.objects.order_by("-date").all())
    event_images = EventImage.objects.all()[:9]
    page_obj = Paginator(all_events, 3)
    if request.method == 'POST':
        page = page_obj.page(int(request.body.decode()))
        return HttpResponse(render(request, 'ajax.html', {"page_obj": page.object_list, "num_pages": range(page_obj.num_pages)}))
    page = page_obj.page(1)
    most_recent_categories = sorted([i for i in Category.objects.all()],
                                    key=lambda x: x.post_set.count())[::-1][:5]

    return render(request, 'index.html', {"event_images": event_images, "Posts": all_Posts, "all_events": all_events, "page_obj": page.object_list, "num_pages": range(page_obj.num_pages), 'recent_categories': most_recent_categories})


@csrf_exempt
def search(request):
    all_Posts = list(Post.objects.order_by("-date").all()[:3])
    search_result = list(Post.objects.order_by(
        "-date").filter(text__icontains=request.GET.get("search_term"), title__icontains=request.GET.get("search_term")).all())
    event_images = EventImage.objects.all()[:9]
    page_obj = Paginator(search_result, 3)
    if request.method == 'POST':
        page = page_obj.page(int(request.body.decode()))
        return HttpResponse(render(request, 'ajax.html', {"page_obj": page.object_list, "num_pages": range(page_obj.num_pages)}))
    page = page_obj.page(1)
    most_recent_categories = sorted([i for i in Category.objects.all()],
                                    key=lambda x: x.post_set.count())[::-1][:5]

    return render(request, 'search.html', {"event_images": event_images, "Posts": all_Posts, "search_result": search_result, "page_obj": page.object_list, "num_pages": range(page_obj.num_pages), 'recent_categories': most_recent_categories})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

def login_user(request):
    if request.is_ajax():
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=name, password=password)
            print(user)
            if user:
                login(request, user)
                return HttpResponse('ok')
            else:
                return HttpResponse('wrong')
    return Http404()


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

    most_recent_categories = sorted([i for i in Category.objects.all()],
                                    key=lambda x: x.post_set.count())[::-1][:5]

    return render(request, 'category.html', {"event_images": event_images, "categoryName": categoryName, "latest_Posts": latest_Posts, "all_Posts": all_Posts, "page_obj": page.object_list, "num_pages": range(page_obj.num_pages), 'recent_categories': most_recent_categories})


def post(request):
    post = Post.objects.get(pk=request.GET.get("id"))
    hit_count = HitCount.objects.get_for_object(post)
    res = HitCountMixin.hit_count(request, hit_count)  # count hit
    latest_Posts = list(Post.objects.order_by("-date").all()[:3])
    author_Posts = list(Post.objects.order_by(
        "-date").filter(author=post.author.id)[:2])
    event_images = EventImage.objects.all()[:9]
    comments = list(Comment.objects.order_by(
        "-date").filter(post=post.id, approved=True))

    most_recent_categories = sorted([i for i in Category.objects.all()],
                                    key=lambda x: x.post_set.count())[::-1][:5]

    return render(request, "post.html", {"event_images": event_images, "comments": comments, "author_Posts": author_Posts, "post": post, "latest_Posts": latest_Posts, 'recent_categories': most_recent_categories, 'categories': post.category.all(), 'hits': post.hit_count.hits})


def event(request):
    event_ = Event.objects.get(pk=request.GET.get("id"))
    hit_count = HitCount.objects.get_for_object(event_)
    res = HitCountMixin.hit_count(request, hit_count)  # count hit
    latest_Posts = list(Post.objects.order_by("-date").all()[:3])
    author_Posts = [post for author in event_.presenters.all() for post in Post.objects.order_by("-date").filter(author=author)[:2]] 
    event_images = EventImage.objects.all()[:9]
    comments = list(Comment.objects.order_by(
        "-date").filter(post=event_.id))
    most_recent_categories = sorted([i for i in Category.objects.all()],
                                    key=lambda x: x.post_set.count())[::-1][:5]
    return render(request, "event.html", {"event_images": event_images, "comments": comments, "author_Posts": author_Posts, "event": event_, "latest_Posts": latest_Posts, 'recent_categories': most_recent_categories, 'hits': event_.hit_count.hits})


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
        if user is not None and not request.user.is_authenticated:
            login(request, user)
            request.session["user"] = name
            return redirect("/")
        elif request.user.is_authenticated:
            return redirect("/")
    else:
        return render(request, "login_form.html", {"error": "please complate the form corectly ..."})


def add_comment(request):
    if request.method == "POST":
        comment_form = SubmitComment(request.POST)
        if comment_form.is_valid():
            post = get_object_or_404(Post, pk=request.POST['post'])
            comment = Comment(author=request.POST['name'], text=request.POST['text'],
                              post=post, approved=False)
            comment.save()
            return HttpResponse('ok')
    return Http404()


@csrf_exempt
def newsletter(request):
    email = NewsLetter(email=request.body.decode(), date=datetime.now())
    email.save()
    return HttpResponse(status=200)

@login_required
@csrf_exempt # more work TODO (for Mehrshad)
def update_profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = UpdateProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = Profile.objects.filter(user=request.user)
                expertise = form.cleaned_data.get('expertise')
                description=form.cleaned_data.get('description')

                if not profile:
                    new_profile = Profile(user=request.user, profession=expertise, 
                                            description=description)
                else:
                    new_profile = profile[0]
                    new_profile.profession = expertise
                    new_profile.description = description
                request.user.first_name = form.cleaned_data.get('first_name')
                request.user.last_name = form.cleaned_data.get('last_name')
                if form.cleaned_data['photo']:
                    new_profile.profile_picture = form.cleaned_data['photo']
                new_profile.save()
                request.user.save()
                return HttpResponse('ok')
                # if Profile.objects.filter(user=request.user)
    return Http404()

def gallery(request):
    photos = EventImage.objects.all()
    return render(request, "gallery.html", {"photos": photos})

def about_us(request):
    authors = [i.user for i in Profile.objects.filter(is_author=True)]
    return render(request, 'about-us.htm', {'authors': authors})