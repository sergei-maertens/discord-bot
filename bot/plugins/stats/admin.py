from django.contrib import admin

from .models import LoggedMessage


@admin.register(LoggedMessage)
class LoggedMessageAdmin(admin.ModelAdmin):
    list_display = ['member_username', 'num_lines']
    list_filter = ['channel', 'member_username']
    ordering = ['-timestamp']
    readonly_fields = [field.name for field in LoggedMessage._meta.get_fields()]
