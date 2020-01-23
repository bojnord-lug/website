from django.contrib import admin
from .models import NewsLetter, EventImage, Category, Comment, Event, Post, Profile, Banners, SubComment

def approve(admin_model, request, query):
    query.update(approved=True)
approve.short_description = "تایید دیدگاه ها"

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('approved',)
    list_display = ('author', 'text')
    actions = [approve]

admin.site.register(NewsLetter)
admin.site.register(Post)
admin.site.register(EventImage)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Banners)
admin.site.register(SubComment)
