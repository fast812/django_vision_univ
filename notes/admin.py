# notes/admin.py
from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "created_at", "updated_at")
    search_fields = ("title", "course", "content")
    list_filter = ("course", "created_at")
