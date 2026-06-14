from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'mood', 'created_at')
    list_filter = ('mood', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основное', {
            'fields': ('author', 'title', 'content')
        }),
        ('Детали', {
            'fields': ('mood', 'created_at', 'updated_at')
        }),
    )
