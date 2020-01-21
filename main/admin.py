from django.contrib import admin
from .models import NewsLetter, EventImage, Authors, Category, Comment, Event, Post, Profile, Banners, SubComment

admin.site.register(NewsLetter)
admin.site.register(Post)
admin.site.register(EventImage)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Banners)
admin.site.register(SubComment)
admin.site.register(Authors)
