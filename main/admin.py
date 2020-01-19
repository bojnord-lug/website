from django.contrib import admin
from .models import Comment, Event, news, Profile, Category, PostImage, SubComment


admin.site.register(news)
admin.site.register(Comment)
admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(PostImage)
admin.site.register(SubComment)
'''@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(SubComment)
class SubCommentAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(news)
class newsAdmin(admin.ModelAdmin):
    list_display = ("title", "date",)
    ordring = ("date")'''
