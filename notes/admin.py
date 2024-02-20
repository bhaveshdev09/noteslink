from django.contrib import admin
from notes.models import Note, NoteChange


class NoteAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "owner", "created_at", "updated_at"]


class NoteChangeAdmin(admin.ModelAdmin):
    fields = ("note", "user", "timestamp", "changes")
    readonly_fields = ("changes",)


admin.site.register(Note, NoteAdmin)
admin.site.register(NoteChange)
