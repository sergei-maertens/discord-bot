from django.contrib import admin

from .models import Command, CommandAction


class CommandActionInline(admin.TabularInline):
    model = CommandAction
    extra = 1


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'description']
    inlines = [CommandActionInline]
