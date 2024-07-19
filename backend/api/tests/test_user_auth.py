from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.refresh_url = reverse("refresh")
        self.profile_url = reverse("profile-actions")
        self.change_password_url = reverse("password-change")
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Testpassword123!",
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
            "password": "Newpassword123!",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.count(), 2
        )  # One user is created in setUp, one in the test
        self.assertEqual(response.data["username"], new_user_data["username"])

    def test_unique_username_registration(self):
        # Try to create another user with the same username
        new_user_data = {
            "username": "testuser",  # same username as self.user_data
            "email": "newuser@example.com",
            "password": "Newpassword123!",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertEqual(
            response.data["username"][0], "A user with that username already exists."
        )

    def test_unique_email_registration(self):
        # Try to create another user with the same email
        new_user_data = {
            "username": "newuser",
            "email": "testuser@example.com",  # same email as self.user_data
            "password": "Newpassword123!",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(
            response.data["email"][0], "A user with that email already exists."
        )

    def test_user_login(self):
        # Attempt to login with incorrect credentials
        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Attempt to login with correct credentials
        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        # Attempt to refresh token without logging in
        response = self.client.post(self.refresh_url, {"refresh": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login the user to get the JWT token
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        refresh_token = login_response.data["refresh"]

        # Use the refresh token to get a new access token
        response = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_profile_view(self):
        # Unauthenticated user trying to view profile
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login the user to get the JWT token
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data["access"]

        # Use the token to access the profile
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["first_name"], self.user_data["first_name"])
        self.assertEqual(response.data["last_name"], self.user_data["last_name"])

    def test_user_profile_update(self):
        # Unauthenticated user trying to update profile
        updated_data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User"
        }
        response = self.client.put(self.profile_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login the user to get the JWT token
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data["access"]

        # Use the token to access the profile
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # Update user profile
        response = self.client.put(self.profile_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], updated_data["username"])
        self.assertEqual(response.data["email"], updated_data["email"])
        self.assertEqual(response.data["first_name"], updated_data["first_name"])
        self.assertEqual(response.data["last_name"], updated_data["last_name"])

        updated_data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "password": "random-password"
        }
        response = self.client.put(self.profile_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile_delete(self):
        # Unauthenticated user trying to delete profile
        response = self.client.delete(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login the user to get the JWT token
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data["access"]

        # Use the token to access the profile
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # Delete user profile
        response = self.client.delete(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)  # No users should exist in the database

    def test_change_password(self):
        # Unauthenticated user trying to change password
        response = self.client.post(self.change_password_url, {
            "old_password": "Testpassword123!",
            "new_password": "Newpassword123!"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login the user to get the JWT token
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data["access"]

        # Use the token to change the password
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # Correct old password
        response = self.client.post(self.change_password_url, {
            "old_password": "Testpassword123!",
            "new_password": "Newpassword123!"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password changed successfully")

        # Verify the new password works
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": "Newpassword123!",
            },
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Incorrect old password
        response = self.client.post(self.change_password_url, {
            "old_password": "wrongpassword",
            "new_password": "Anotherpassword123!"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Incorrect old password")
