from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from notes.models import Note, NoteChange

User = get_user_model()


class CreateNoteViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.create_note_url = reverse("create_note")
        self.valid_payload = {"content": "Test note content", "title": "Test note 1"}

    def test_create_note_authenticated(self):
        response = self.client.post(
            self.create_note_url, self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Note.objects.filter(owner=self.user, content="Test note content").exists()
        )

    def test_create_note_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.create_note_url, self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(
            Note.objects.filter(owner=self.user, content="Test note content").exists()
        )


class RetrieveUpdateNoteViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(
            owner=self.user, content="Test note content", title="Test note 1"
        )
        self.retrieve_update_note_url = reverse(
            "retrieve_update_note", kwargs={"pk": self.note.pk}
        )
        self.valid_payload = {"content": "Updated note content"}

    def test_retrieve_note_authenticated(self):
        response = self.client.get(self.retrieve_update_note_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Test note content")

    def test_update_note_authenticated(self):
        response = self.client.put(
            self.retrieve_update_note_url, self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.content, "Updated note content")

    def test_retrieve_update_note_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.retrieve_update_note_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ShareNoteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )
        self.note = Note.objects.create(
            title="Test Note", content="Test content", owner=self.user
        )
        self.share_note_url = reverse("share_note")

    def test_share_note_successful(self):
        # Create another user
        another_user = User.objects.create_user(
            username="anotheruser",
            password="anotherpassword",
            email="anotheruser@example.com",
        )
        # Login as the original user
        self.client.force_authenticate(user=self.user)
        # Send a POST request to share the note with the new user
        data = {"note": self.note.pk, "users": [another_user.pk]}
        response = self.client.post(self.share_note_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the note is shared with the new user
        self.assertTrue(self.note.shared_with.filter(pk=another_user.pk).exists())

    def test_share_note_without_users(self):
        self.client.force_authenticate(user=self.user)
        data = {"note": self.note.pk, "users": []}  # Sending empty list of users
        response = self.client.post(self.share_note_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "users", response.data
        )  # Check if the error message contains 'users'

    def test_share_note_with_owner(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "note": self.note.pk,
            "users": [self.user.pk],  # Trying to share note with its owner
        }
        response = self.client.post(self.share_note_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the note is not shared with its owner
        self.assertFalse(self.note.shared_with.filter(pk=self.user.pk).exists())

    def test_share_note_with_invalid_note_id(self):
        self.client.force_authenticate(user=self.user)
        invalid_note_id = 9999  # Assuming this ID does not exist in the database
        data = {"note": invalid_note_id, "users": [self.user.pk]}
        response = self.client.post(self.share_note_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_share_note_with_invalid_user_ids(self):
        self.client.force_authenticate(user=self.user)
        invalid_user_id = 9999  # Assuming this ID does not exist in the database
        data = {"note": self.note.pk, "users": [invalid_user_id]}
        response = self.client.post(self.share_note_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TrackNoteChangesSignalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.note = Note.objects.create(
            owner=self.user, title="Test Note", content="Original content"
        )

    def test_track_note_changes_signal(self):
        initial_count = NoteChange.objects.count()
        new_content = "Updated content"
        self.note.content = new_content
        self.note.save()
        updated_count = NoteChange.objects.count()
        self.assertEqual(updated_count, initial_count + 1)

        # Retrieve the created NoteChange object
        change = NoteChange.objects.latest("timestamp")
        self.assertEqual(change.note, self.note)
        self.assertEqual(change.user, self.user)
        # self.assertEqual(
        #     change.changes,
        #     [{"type": "added", "content": "Updated content"}],
        # )
