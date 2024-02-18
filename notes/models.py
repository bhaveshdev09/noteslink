from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Note(models.Model):
    owner = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)
    content = models.TextField()
    shared_with = models.ManyToManyField(User, related_name="shared_notes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.owner.get_username()}"
