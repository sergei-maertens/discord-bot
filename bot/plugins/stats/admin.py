from django.contrib import admin

from .models import Download, GameSession, LoggedMessage


@admin.register(LoggedMessage)
class LoggedMessageAdmin(admin.ModelAdmin):
    list_display = ['member_username', 'num_lines']
    list_filter = ['channel', 'member_username']
    ordering = ['-timestamp']
    readonly_fields = [field.name for field in LoggedMessage._meta.get_fields()]


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['member', 'game', 'start', 'duration']
    list_filter = ['game', 'member']
    ordering = ['-start']


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']
    list_filter = ['created']
    ordering = ['-created']
