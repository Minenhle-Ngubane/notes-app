from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_favourite", "updated_at")
    list_filter = ("is_favourite", "created_at", "updated_at")
    search_fields = ("title", "description", "owner__email")
    ordering = ("-updated_at",)