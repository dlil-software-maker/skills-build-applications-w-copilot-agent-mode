from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Profile


class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test user bio',
            age=28,
            weight=70.5,
            height=175.0,
            fitness_goals='Run a half marathon',
        )

    def test_profile_created(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.age, 28)

    def test_profile_api_list(self):
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)
