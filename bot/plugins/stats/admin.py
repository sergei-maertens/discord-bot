from django.contrib import admin

from .models import LoggedMessage


@admin.register(LoggedMessage)
class LoggedMessageAdmin(admin.ModelAdmin):
    list_display = ['member_username']
    list_filter = ['channel']
