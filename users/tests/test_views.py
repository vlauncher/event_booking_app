from django.test import TestCase, Client
from ..models import User, Profile
from django.urls import reverse


# Create your tests here.
class TestHomePage(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class TestRegisterView(TestCase):
    def test_register_view(self):
        url = reverse("register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_post_valid(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.post(reverse("register"), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class TestLoginView(TestCase):
    def test_login_view(self):
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_post_valid(self):
        User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="test@example.com",
            password="password123",
            is_active=True,
        )
        form_data = {"email": "test@example.com", "password": "password123"}
        response = self.client.post(reverse("login"), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
