from django.contrib import admin

from .models import Channel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'allow_nsfw')
    list_filter = ('allow_nsfw',)
    search_fields = ('name',)
