from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    RegisterView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    UpdateProfileView,
    ListProfileView,
    VerifyEmailView,
    HomePageView,
)


class TestUrls(SimpleTestCase):

    def test_register_url_is_resolved(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_change_password_url_is_resolved(self):
        url = reverse("change_password")
        self.assertEqual(resolve(url).func.view_class, ChangePasswordView)

    def test_update_profile_url_is_resolved(self):
        url = reverse("update_profile")
        self.assertEqual(resolve(url).func.view_class, UpdateProfileView)

    def test_list_profile_url_is_resolved(self):
        url = reverse("list_profile")
        self.assertEqual(resolve(url).func.view_class, ListProfileView)

    def test_verify_email_url_is_resolved(self):
        url = reverse("verify_email", args=["123", "abc"])
        self.assertEqual(resolve(url).func.view_class, VerifyEmailView)

    def test_home_url_is_resolved(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func.view_class, HomePageView)
