from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path("profile/", views.profile, name='profile'),

    path("contact/", views.contact, name='contact'),

    path("category/", views.category, name='category'),

    path("contact/", views.contact, name='single'),
]
