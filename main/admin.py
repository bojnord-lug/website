from django.contrib import admin
from .models import news,Profile


admin.site.register(Profile)

@admin.register(news)
class newsAdmin(admin.ModelAdmin):
    list_display=("title","date",)
    ordring=("date")