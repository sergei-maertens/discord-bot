from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['member', 'text', 'deliver_at', 'delivered']
    list_filter = ['deliver_at']
    search_fields = ['member__name', 'member__discord_id', 'text']
