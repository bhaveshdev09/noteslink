from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from notes.utils import calculate_changes

User = get_user_model()


class Note(models.Model):
    owner = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="")
    content = models.TextField()
    shared_with = models.ManyToManyField(User, related_name="shared_notes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.title}"


class NoteChange(models.Model):
    note = models.ForeignKey("Note", on_delete=models.CASCADE, related_name="changes")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Change made to Note {self.note.id} at {self.timestamp} by {self.user.username}"


@receiver(pre_save, sender=Note)
def track_note_changes(sender, instance, **kwargs):
    if instance.id:
        # Get the changes made to the note
        current_content = instance.content
        previous_content = sender.objects.get(id=instance.id).content

        # Compare the changes to the note
        has_changed, changes = calculate_changes(current_content, previous_content)
        if has_changed:
            NoteChange.objects.create(
                note=instance, user=instance.user, changes=changes
            )
