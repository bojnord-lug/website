from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),

    path("profile", views.profile, name='profile'),

    path("contact", views.contact, name='contact'),

    path("category", views.category, name='category'),

    path("post", views.post, name='post'),
    path("event", views.event, name='event'),
    path("bloglist/", views.index)

]
