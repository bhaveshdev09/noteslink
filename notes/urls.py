from django.urls import path
from notes.views import (
    CreateNoteView,
    RetriveUpdateNoteView,
    ShareNoteView,
)

urlpatterns = [
    path("create/", CreateNoteView.as_view(), name="create_note"),
    path("<int:pk>/", RetriveUpdateNoteView.as_view(), name="retrieve_update_note"),
    path("share/", ShareNoteView.as_view(), name="share_note"),
]
