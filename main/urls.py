from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path("login/", views.Login , name='login'),

    path("Signin/" ,views.Signin , name='signin')
]
