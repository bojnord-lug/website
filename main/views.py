import json, requests
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import (Http404, HttpResponseRedirect, get_object_or_404,
                              redirect, render, reverse)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from PIL import Image

from .forms import (CaptchaPasswordResetForm, LoginForm, SubmitComment,EdirForm,
                    UpdateProfileForm, UserRegistrationForm, AddPostForm)
from .models import (Category, Comment, Event, EventImage, NewsLetter, Post,
                     Profile)

from .tasks import post_send_email


@csrf_exempt
def index(request):
    if request.GET.get('login'):
        messages.add_message(request, messages.SUCCESS, "{} عزیز، شما با \
            موفقیت وارد سیستم شدید".format(request.user.first_name))

    if request.GET.get('logout'):
        messages.add_message(request, messages.INFO, "شما از حساب خود خارج شدید")
        
    if request.GET.get('password-reset'):
        messages.add_message(request, messages.SUCCESS, "گذرواژه شما با موفقیت تغییر کرد")
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

    return render(request, 'index.html', {"event_images": event_images, "Posts": all_Posts, "all_events": all_events, "page_obj": page.object_list, "num_pages": range(page_obj.num_pages), 'recent_categories': most_recent_categories, 'token': settings.RECAPTCHA_SITE_KEY})


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
    return redirect('/?logout=true')

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
    if request.user.is_authenticated:
        return render(request, "profile.html")
    else:
        return Http404()  # TODO: Render a more gentle page.


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
    form = LoginForm(request.POST)
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def add_comment(request):
    if request.method == "POST":
        comment_form = SubmitComment(request.POST)
        if comment_form.is_valid():
            url = "https://www.google.com/recaptcha/api/siteverify"
            params = {
                'secret': settings.RECAPTCHA_SECRET_KEY_V2,
                'response': request.POST.get('captcha'),
                'remoteip': get_client_ip(request)
            }
            verify_rs = requests.get(url, params=params, verify=True).json()
            if not verify_rs['success']:
                return HttpResponse('captcha')
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
    return render(request, 'about-us.html', {'authors': authors})

class CaptchaPasswordResetView(PasswordResetView):
    form_class = CaptchaPasswordResetForm

def register(request):
    if request.method=='POST' and request.is_ajax(): 
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data.get('username'), 
                                    form.cleaned_data.get('email'),
                                    form.cleaned_data.get('password1'))
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            print(form.cleaned_data.get('password'))
            # user.email = form.cleaned_data.get('email')
            # user.set_password(form.cleaned_data.get('password1'))
            user.save(form.cleaned_data.get('password'))
            profile = Profile(user=user, profession=form.cleaned_data.get('expertise'))
            profile.save()
            return HttpResponse('success')
        else:
            print(form.errors.as_data().values())
            return HttpResponse(list(form.errors.as_data().values())[0][0])
    return Http404()

  
def new_post(request):
    if request.method=='GET':
        if request.user.is_authenticated:
            if request.user.profile.is_author:
                return render(request, 'new_post.html', {'categories': Category.objects.all()})
        return Http404()
    elif request.method=='POST':
        if request.user.is_authenticated:
            if request.user.profile.is_author:
                new_post = AddPostForm(request.POST, request.FILES)
                if new_post.is_valid():
                    post = Post.objects.create(
                        title = new_post.cleaned_data.get('title'),
                        text = new_post.cleaned_data.get('text'),
                        image = new_post.cleaned_data.get('image'),
                        author = request.user 
                    )
                    for i in new_post.cleaned_data.get('category')[:]:
                        post.category.add(i)
                    post.save()
                    print('redirecting')

                    # res = post_send_email.delay(post.id, post.title) # TODO: check this
                    return HttpResponseRedirect('my-posts')
                else:
                    return HttpResponse('pleas complate all of field')

        return Http404()

      
def my_posts(request):
    if request.user.is_authenticated:
        if request.user.profile.is_author:
            posts = Post.objects.filter(author=request.user)
            return render(request, 'myposts.html', {'posts':posts})
    return Http404()

  
@require_POST
@csrf_exempt
def delelte_post(request, id):
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.profile.is_author:
            post = Post.objects.filter(id=id)[0]
            if post.author == request.user:
                post.delete()
                return HttpResponse(" پست با موفقیت حذف شد")
    return Http404()
        

def edit_post(request, id):
    post = Post.objects.filter(id=id)[0]
    if post.author == request.useruser:
        if request.method == 'GET':
            return render(request, 'new_post.html',{'post':post,'categories': Category.objects.all(), 'type':"edit"})
        elif request.method == 'POST':
            edit = AddPostForm(request.POST, request.FILES)
            if edit.is_valid():
                print('editing')
                post.title = edit.cleaned_data.get('title')
                post.text =edit.cleaned_data.get('text')   
                post.image = edit.cleaned_data.get('image')
                post.category.set(edit.cleaned_data.get('category')[:])
                post.save()
                return render(request, 'new_post.html', {'categories': Category.objects.all(), 'posted': True})
    return Http404()
