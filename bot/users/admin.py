from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', '__str__', 'is_bot', 'can_admin_bot']
    list_filter = ['can_admin_bot', 'is_bot', 'last_seen']
    search_fields = ['discord_id', 'name']
