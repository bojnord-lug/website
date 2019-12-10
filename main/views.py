from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'index.htm')

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
