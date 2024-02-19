from django.contrib import admin
from notes.models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "owner", "created_at"]


admin.site.register(Note, NoteAdmin)
