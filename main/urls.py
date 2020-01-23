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
    path("bloglist/", views.index),
    path("submit_comment", views.add_comment),
    path("saveEmail/", views.newsletter),
    path('update-profile', views.update_profile)

]
