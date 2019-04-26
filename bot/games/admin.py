from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name']
    raw_id_fields = ['alias_for']
    search_fields = ['name']
