from django.contrib import admin

from .models import BotAdmin, Bot


class BotOwner(admin.ModelAdmin):
    list_display = ('chat', 'first_name', 'last_name', 'time',)
    search_fields = ('chat', 'last_name',)
    list_filter = ('chat', 'time',)
    list_editable = ('first_name', 'last_name')

admin.site.register(BotAdmin, BotOwner)
admin.site.register(Bot)
