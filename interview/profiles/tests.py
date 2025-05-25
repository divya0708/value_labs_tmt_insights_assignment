from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileTests(TestCase):

    def test_create_user_success(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='test')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_admin)

    def test_get_full_name(self):
        user = User.objects.create_user(
            email='full@example.com',
            password='testpass',
            first_name='Full',
            last_name='Name'
        )
        self.assertEqual(user.get_full_name(), 'Full Name')

    def test_get_username_returns_email(self):
        user = User.objects.create_user(
            email='email@example.com',
            password='pass'
        )
        self.assertEqual(user.get_username(), 'email@example.com')

    def test_avatar_optional(self):
        user = User.objects.create_user(
            email='avatar@example.com',
            password='avatarpass',
            first_name='Av',
            last_name='Tarr'
        )
        self.assertFalse(user.avatar)

