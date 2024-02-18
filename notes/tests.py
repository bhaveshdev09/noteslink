from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateNoteViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.create_note_url = reverse("create_note")
        self.valid_payload = {"content": "Test note content"}

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


class RetrieveUpdateNoteViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(owner=self.user, content="Test note content")
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
