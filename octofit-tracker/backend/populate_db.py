import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard

# Create test users
def create_users():
    users = []
    for i in range(1, 4):
        user, created = User.objects.get_or_create(username=f'user{i}', defaults={'email': f'user{i}@test.com'})
        user.set_password('testpass123')
        user.save()
        users.append(user)
    return users

# Create test teams
def create_teams(users):
    team1, _ = Team.objects.get_or_create(name='Team Alpha')
    team2, _ = Team.objects.get_or_create(name='Team Beta')
    team1.members.set(users[:2])
    team2.members.set(users[1:])
    team1.save()
    team2.save()
    return [team1, team2]

# Create test activities
def create_activities(users, teams):
    Activity.objects.get_or_create(user=users[0], activity_type='Running', duration=30, calories_burned=300, date=datetime.date.today(), team=teams[0])
    Activity.objects.get_or_create(user=users[1], activity_type='Cycling', duration=45, calories_burned=450, date=datetime.date.today(), team=teams[1])
    Activity.objects.get_or_create(user=users[2], activity_type='Swimming', duration=60, calories_burned=600, date=datetime.date.today(), team=None)

# Create test workouts
def create_workouts(users):
    workout1, _ = Workout.objects.get_or_create(name='Cardio Blast', description='High intensity cardio workout', difficulty='Medium')
    workout2, _ = Workout.objects.get_or_create(name='Strength Builder', description='Full body strength training', difficulty='Hard')
    workout1.suggested_for.set(users[:2])
    workout2.suggested_for.set(users[1:])
    workout1.save()
    workout2.save()
    return [workout1, workout2]

# Create leaderboard entries
def create_leaderboard(teams):
    for team in teams:
        Leaderboard.objects.get_or_create(team=team, score=100 * (teams.index(team) + 1))

def main():
    users = create_users()
    teams = create_teams(users)
    create_activities(users, teams)
    create_workouts(users)
    create_leaderboard(teams)
    print('Test data created successfully.')

if __name__ == '__main__':
    main()
