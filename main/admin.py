from django.contrib import admin
from .models import Category, Comment, Event, Post, Profile, PostImage, SubComment


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(PostImage)
admin.site.register(SubComment)
