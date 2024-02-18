from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser


class UserSignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("signup")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, "testuser")

    def test_user_signup_invalid_data(self):
        response = self.client.post(
            self.signup_url,
            {"username": "", "email": "invalidemail", "password": ""},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        CustomUser.objects.create_user(**self.user_data)

    def test_user_login(self):
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in response.data)
        self.assertTrue("access" in response.data)

    def test_user_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
