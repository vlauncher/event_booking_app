from ..forms import (
    RegisterForm,
    CustomLoginForm,
    ChangePasswordForm,
    UpdateProfileForm,
    RegisterForm,
)
from django.test import TestCase
from django.urls import reverse
from ..models import User, Profile


class TestRegisterForm(TestCase):

    def setUp(self):
        self.data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "w5kFV@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }

    def test_form_valid(self):
        form = RegisterForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form = RegisterForm(data=self.data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "w5kFV@example.com")


class TestCustomLoginForm(TestCase):

    def setUp(self):
        User.objects.create_user(
            email="w5kFV@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            is_active=True,
        )

    def test_form_valid(self):
        form = CustomLoginForm(
            data={"email": "w5kFV@example.com", "password": "password123"}
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = CustomLoginForm(
            data={"email": "w5kFV@example.com", "password": "wrongpassword"}
        )
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form = CustomLoginForm(
            data={"email": "w5kFV@example.com", "password": "password123"}
        )
        self.assertTrue(form.is_valid())
        user = form.get_user()
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "w5kFV@example.com")


class TestChangePasswordForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="w5kFV@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            is_active=True,
        )

    def test_form_valid(self):
        form = ChangePasswordForm(
            user=self.user,
            data={
                "current_password": "password123",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = ChangePasswordForm(
            user=self.user,
            data={
                "current_password": "wrongpassword",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
        )
        self.assertFalse(form.is_valid())

    def test_valid_password_change(self):
        form = ChangePasswordForm(
            user=self.user,
            data={
                "current_password": "password123",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
        )
        self.assertTrue(form.is_valid())
        form.user.set_password(form.cleaned_data["new_password"])
        form.user.save()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_invalid_password_change(self):
        form = ChangePasswordForm(
            user=self.user,
            data={
                "current_password": "wrongpassword",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
        )
        self.assertFalse(form.is_valid())
        form.user.set_password(form.cleaned_data["new_password"])
        form.user.save()
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("newpassword123"))

    def test_invalid_password_change(self):
        form = ChangePasswordForm(
            user=self.user,
            data={
                "current_password": "wrongpassword",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
        )
        self.assertFalse(form.is_valid())


class TestUpdateProfileForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="w5kFV@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            is_active=True,
        )

        self.profile = Profile.objects.get_or_create(
            user=self.user,
            defaults={"address": "123 Test St", "phone_number": "1234567890"},
        )

    def test_form_valid(self):
        form = UpdateProfileForm(
            data={"address": "456 Test St", "phone_number": "9876543210"}
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = UpdateProfileForm(data={"address": "", "phone_number": ""})
        self.assertFalse(form.is_valid())
