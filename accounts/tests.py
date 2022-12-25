from django.test import TestCase

# Create your tests here.


class TestUser(TestCase):
    def test_user(self):
        self.assertEqual(1, 1)

    def test_admin_creation(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_superuser(
            email='admin@admin.com',
            password='123',
            username='admin'
        )

        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_onboarded, True)
