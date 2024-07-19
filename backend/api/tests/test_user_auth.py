from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_url = reverse('refresh')
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
        self.user = User.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
        )

    def test_user_registration(self):
        # Create a new user for registration test
        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # One user is created in setUp, one in the test
        self.assertEqual(response.data['username'], new_user_data['username'])

    def test_user_login(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        refresh_token = login_response.data['refresh']
        response = self.client.post(self.refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
