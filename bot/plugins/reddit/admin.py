from django.contrib import admin

from .models import RedditCommand


@admin.register(RedditCommand)
class RedditCommandAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'command', 'times_used', 'nsfw')
    list_filter = ('nsfw',)
    search_fields = ('command', 'subreddit')
