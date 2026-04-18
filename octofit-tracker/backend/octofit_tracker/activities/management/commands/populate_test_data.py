from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile
from teams.models import Team
from activities.models import Activity
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate database with test data...'))

        # Clear existing data
        User.objects.all().delete()
        Profile.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()

        # Create test users
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_johnson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Johnson'},
            {'username': 'sarah_williams', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Williams'},
            {'username': 'alex_brown', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Brown'},
        ]

        users = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password='testpassword123'
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # Create user profiles
        profile_data = [
            {'bio': 'Fitness enthusiast and gym lover', 'age': 28, 'weight': 75.5, 'height': 180, 'fitness_goals': 'Build muscle'},
            {'bio': 'Marathon runner', 'age': 32, 'weight': 62.0, 'height': 168, 'fitness_goals': 'Improve endurance'},
            {'bio': 'Yoga instructor', 'age': 29, 'weight': 65.0, 'height': 170, 'fitness_goals': 'Flexibility and balance'},
            {'bio': 'CrossFit enthusiast', 'age': 26, 'weight': 70.0, 'height': 175, 'fitness_goals': 'Strength and conditioning'},
            {'bio': 'Recreational athlete', 'age': 31, 'weight': 80.0, 'height': 185, 'fitness_goals': 'General fitness'},
        ]

        for user, profile_info in zip(users, profile_data):
            profile = Profile.objects.create(
                user=user,
                bio=profile_info['bio'],
                age=profile_info['age'],
                weight=profile_info['weight'],
                height=profile_info['height'],
                fitness_goals=profile_info['fitness_goals']
            )
            self.stdout.write(f'Created profile for: {user.username}')

        # Create teams
        team_data = [
            {'name': 'Morning Warriors', 'description': 'Early morning fitness group'},
            {'name': 'Canyon Runners', 'description': 'Trail running enthusiasts'},
            {'name': 'Strength Squad', 'description': 'Weight lifting and strength training'},
        ]

        teams = []
        for team_info in team_data:
            team = Team.objects.create(
                name=team_info['name'],
                description=team_info['description'],
                created_by=users[0]
            )
            # Add members to team
            team.members.add(*random.sample(users, k=random.randint(2, 4)))
            teams.append(team)
            self.stdout.write(f'Created team: {team.name}')

        # Create activities
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Walking', 'Hiking']
        base_date = datetime.now() - timedelta(days=30)

        for user in users:
            for i in range(random.randint(5, 10)):
                activity_date = base_date + timedelta(days=random.randint(0, 30))
                activity = Activity.objects.create(
                    user=user,
                    activity_type=random.choice(activity_types),
                    duration=random.randint(15, 120),
                    calories_burned=random.randint(200, 800),
                    date=activity_date,
                    notes=f'Great {activity_types[0].lower()} session!'
                )
                self.stdout.write(f'Created activity for {user.username}: {activity.activity_type}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with test data!'))
