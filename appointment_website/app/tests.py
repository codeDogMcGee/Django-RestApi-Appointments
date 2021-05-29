from django.contrib.auth import get_user_model
from django.test import TestCase

class UsersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='customer@customer.com', phone='5555555', name='customer', password='test')
        self.assertEqual(user.email, 'customer@customer.com')
        self.assertEqual(user.phone, '5555555')
        self.assertEqual(user.name, 'customer')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for AbstractUser
            # username does not exist for AbstractBaseUser
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(TypeError):
            User.objects.create_user(phone='')
        with self.assertRaises(TypeError):
            User.objects.create_user(name='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', phone='', name='', password='test')


