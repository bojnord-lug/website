from django.shortcuts import render, redirect,reverse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import Log_in,Sign_in
from .models import news

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET

def index(request):
    all_news=list(news.objects.all())
    return render(request, 'index.htm',{"news":all_news[::-1]})

def login_user(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'login.htm')


def login_form(request):
    return render(request,"login_form")

@require_POST
@csrf_exempt
def Signin(request):
    u=request.POST.get('name')
    e=request.POST.get('email')
    p=request.POST.get('passwd')
    person=authenticate(request,username=u,password=p)
    if person is not None:
        return render(request,"sign_in.html",{"error":"this accont is already ."})
    elif u=="" or e=="" or p=="":
        return render(request,"sign_in.html",{"error":"Please complate the form"})
    else:
        user=User.objects.create_user(u,e,p)
        user.save()
        login(request,user)
        request.session["user"]=u
        return HttpResponseRedirect("/")


@require_POST
@csrf_exempt
def Login(request):
    form=Log_in(request.POST)
    if form.is_valid():
        name=form.cleaned_data.get("username")
        paswd=form.cleaned_data.get("passwd")
        user=authenticate(request,username=name,password=paswd)
        if user is not None and not request.user.is_authenthicated:
            login(request,user)
            request.session["user"]=name
            return redirect("/")
        elif request.user.is_authenthicated:
            return redirect("/")
    else:
        return render(request,"login_form.html",{"error":"please complate the form corectly ..."})


