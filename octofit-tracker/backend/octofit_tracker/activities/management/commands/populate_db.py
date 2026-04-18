from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile
from teams.models import Team
from activities.models import Activity
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate octofit_db with test data...'))

        # Clear old data
        Activity.objects.all().delete()
        Team.objects.all().delete()
        Profile.objects.all().delete()
        normal_user_ids = [user.pk for user in User.objects.all() if not user.is_superuser]
        if normal_user_ids:
            User.objects.filter(pk__in=normal_user_ids).delete()

        # Create superhero users and profiles
        heroes = [
            {'username': 'tony_stark', 'email': 'tony@starkindustries.com', 'first_name': 'Tony', 'last_name': 'Stark', 'bio': 'Genius inventor and ironman.', 'age': 48, 'weight': 102.5, 'height': 185, 'fitness_goals': 'Stay in peak armor shape'},
            {'username': 'steve_rogers', 'email': 'steve@avengers.com', 'first_name': 'Steve', 'last_name': 'Rogers', 'bio': 'Super soldier with endless stamina.', 'age': 105, 'weight': 100.0, 'height': 188, 'fitness_goals': 'Lead the team and stay strong'},
            {'username': 'diana_prince', 'email': 'diana@themiscira.com', 'first_name': 'Diana', 'last_name': 'Prince', 'bio': 'Amazonian warrior with great balance.', 'age': 3000, 'weight': 75.0, 'height': 183, 'fitness_goals': 'Train for justice and agility'},
            {'username': 'bruce_wayne', 'email': 'bruce@wayneenterprises.com', 'first_name': 'Bruce', 'last_name': 'Wayne', 'bio': 'Vigilante who trains every night.', 'age': 42, 'weight': 95.0, 'height': 188, 'fitness_goals': 'Prepare for Gotham missions'},
            {'username': 'barry_allen', 'email': 'barry@starlabs.com', 'first_name': 'Barry', 'last_name': 'Allen', 'bio': 'Speedster with super fast recovery.', 'age': 29, 'weight': 85.0, 'height': 191, 'fitness_goals': 'Keep speed and endurance high'},
        ]

        users = []
        for hero in heroes:
            user = User.objects.create_user(
                username=hero['username'],
                email=hero['email'],
                first_name=hero['first_name'],
                last_name=hero['last_name'],
                password='testpassword123'
            )
            Profile.objects.create(
                user=user,
                bio=hero['bio'],
                age=hero['age'],
                weight=hero['weight'],
                height=hero['height'],
                fitness_goals=hero['fitness_goals'],
            )
            users.append(user)
            self.stdout.write(f'Created superhero user: {user.username}')

        # Create Marvel and DC teams
        marvel_team = Team.objects.create(name='Team Marvel', description='Superheroes from the Marvel universe.', created_by=users[0])
        dc_team = Team.objects.create(name='Team DC', description='Heroes from the DC universe.', created_by=users[2])
        marvel_team.members.add(users[0], users[1])
        dc_team.members.add(users[2], users[3], users[4])

        self.stdout.write('Created Team Marvel and Team DC')

        # Create activities for each hero
        activity_options = ['Flight Training', 'Speed Drills', 'Combat Practice', 'Strength Conditioning', 'Stealth Work', 'Tactical Planning']
        base_date = datetime.now() - timedelta(days=20)

        for user in users:
            for index in range(5):
                Activity.objects.create(
                    user=user,
                    activity_type=random.choice(activity_options),
                    duration=random.randint(25, 90),
                    calories_burned=random.randint(250, 760),
                    date=base_date + timedelta(days=index * 3),
                    notes=f'Hero training session #{index + 1}',
                )
            self.stdout.write(f'Created activities for {user.username}')

        self.stdout.write(self.style.SUCCESS('Successfully populated octofit_db with test data'))
