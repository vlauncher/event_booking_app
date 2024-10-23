from django.test import TestCase
from django.urls import reverse
from ..models import User, Profile


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="testpassword",
            is_active=True,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)


class ProfileModelTest(TestCase):

    def test_profile_creation(self):
        user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="testpassword",
            is_active=True,
        )
        profile = Profile.objects.get_or_create(
            user=user, defaults={"address": "123 Test St", "phone_number": "1234567890"}
        )

    def test_profile_update(self):
        user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="testpassword",
            is_active=True,
        )
        profile, created = Profile.objects.get_or_create(
            user=user, defaults={"address": "123 Test St", "phone_number": "1234567890"}
        )
        profile.address = "123 Test St"
        profile.phone_number = "1234567890"
        profile.save()
        self.assertEqual(profile.address, "123 Test St")
        self.assertEqual(profile.phone_number, "1234567890")
