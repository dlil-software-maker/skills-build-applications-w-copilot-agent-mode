from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Activity


class ActivityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='activityuser', password='pass123')
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=45,
            calories_burned=420,
            notes='Evening run in the park',
        )

    def test_activity_created(self):
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.calories_burned, 420)

    def test_activity_api_list(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['activity_type'], 'Running')
