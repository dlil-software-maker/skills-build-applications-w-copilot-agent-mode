from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Team


class TeamTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.creator = User.objects.create_user(username='teamcreator', password='pass123')
        self.member = User.objects.create_user(username='teammember', password='pass123')
        self.team = Team.objects.create(
            name='Alpha Team',
            description='A competitive fitness group',
            created_by=self.creator,
        )
        self.team.members.add(self.creator, self.member)

    def test_team_created(self):
        self.assertEqual(self.team.name, 'Alpha Team')
        self.assertEqual(self.team.members.count(), 2)

    def test_team_api_list(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Alpha Team')
