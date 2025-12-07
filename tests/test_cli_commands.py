import pytest
from unittest.mock import Mock
import tempfile
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import (
    cli_create_user, cli_create_workout, cli_list, cli_get,
    cli_update_user, cli_update_workout, cli_delete_user, cli_delete_workout,
    cli_list_users, cli_list_workouts, cli_schedule, repo
)
from repository.repository import Repository
import main


@pytest.fixture
def temp_repo():
    """Create temporary repository for isolated testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    old_repo = main.repo
    main.repo = Repository(filename=path)
    yield main.repo
    main.repo = old_repo
    if os.path.exists(path):
        os.unlink(path)


class TestCLICommands:
    """Test CLI command functions."""

    def test_cli_create_user(self, temp_repo, capsys):
        args = Mock()
        args.username = "TestUser"
        args.age = 25
        args.height = 170.0
        args.weight = 70.0
        
        cli_create_user(args)
        
        captured = capsys.readouterr()
        assert "Created user id=" in captured.out

    def test_cli_create_workout(self, temp_repo, capsys):
        args = Mock()
        args.name = "Test Workout"
        args.duration = 30
        
        cli_create_workout(args)
        
        captured = capsys.readouterr()
        assert "Created workout id=" in captured.out

    def test_cli_list(self, temp_repo, capsys):
        # Create some records first
        temp_repo.create({"username": "User1", "age": 25}, type_="user")
        temp_repo.create({"name": "Workout1", "duration": 30}, type_="workout")
        
        args = Mock()
        cli_list(args)
        
        captured = capsys.readouterr()
        assert "User1" in captured.out or "user" in captured.out.lower()

    def test_cli_get_existing(self, temp_repo, capsys):
        user_id = temp_repo.create({"username": "User1", "age": 25}, type_="user")
        
        args = Mock()
        args.id = user_id
        
        cli_get(args)
        
        captured = capsys.readouterr()
        assert "User1" in captured.out or "user" in captured.out.lower()

    def test_cli_get_not_found(self, temp_repo, capsys):
        args = Mock()
        args.id = "nonexistent"
        
        cli_get(args)
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_cli_update_user(self, temp_repo, capsys):
        user_id = temp_repo.create({"username": "User1", "age": 25}, type_="user")
        
        args = Mock()
        args.id = user_id
        args.username = "UpdatedUser"
        args.age = 26
        args.height = None
        args.weight = None
        
        cli_update_user(args)
        
        captured = capsys.readouterr()
        assert "Updated user" in captured.out

    def test_cli_update_user_not_found(self, temp_repo, capsys):
        args = Mock()
        args.id = "nonexistent"
        args.username = "Test"
        args.age = 25
        args.height = None
        args.weight = None
        
        cli_update_user(args)
        
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_cli_update_workout(self, temp_repo, capsys):
        workout_id = temp_repo.create({"name": "Workout1", "duration": 30}, type_="workout")
        
        args = Mock()
        args.id = workout_id
        args.name = "UpdatedWorkout"
        args.duration = 45
        
        cli_update_workout(args)
        
        captured = capsys.readouterr()
        assert "Updated workout" in captured.out

    def test_cli_delete_user(self, temp_repo, capsys):
        user_id = temp_repo.create({"username": "User1", "age": 25}, type_="user")
        
        args = Mock()
        args.id = user_id
        
        cli_delete_user(args)
        
        captured = capsys.readouterr()
        assert "Deleted user" in captured.out

    def test_cli_delete_user_not_found(self, temp_repo, capsys):
        args = Mock()
        args.id = "nonexistent"
        
        cli_delete_user(args)
        
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_cli_delete_workout(self, temp_repo, capsys):
        workout_id = temp_repo.create({"name": "Workout1", "duration": 30}, type_="workout")
        
        args = Mock()
        args.id = workout_id
        
        cli_delete_workout(args)
        
        captured = capsys.readouterr()
        assert "Deleted workout" in captured.out

    def test_cli_list_users(self, temp_repo, capsys):
        temp_repo.create({"username": "User1", "age": 25}, type_="user")
        temp_repo.create({"username": "User2", "age": 30}, type_="user")
        
        args = Mock()
        cli_list_users(args)
        
        captured = capsys.readouterr()
        assert "Total users: 2" in captured.out

    def test_cli_list_users_empty(self, temp_repo, capsys):
        args = Mock()
        cli_list_users(args)
        
        captured = capsys.readouterr()
        assert "No users found" in captured.out

    def test_cli_list_workouts(self, temp_repo, capsys):
        temp_repo.create({"name": "Workout1", "duration": 30}, type_="workout")
        temp_repo.create({"name": "Workout2", "duration": 45}, type_="workout")
        
        args = Mock()
        cli_list_workouts(args)
        
        captured = capsys.readouterr()
        assert "Total workouts: 2" in captured.out

    def test_cli_list_workouts_empty(self, temp_repo, capsys):
        args = Mock()
        cli_list_workouts(args)
        
        captured = capsys.readouterr()
        assert "No workouts found" in captured.out

    def test_cli_schedule_no_strategy(self, temp_repo, capsys):
        user_id = temp_repo.create({"username": "User1", "age": 25, "weight": 70.0}, type_="user")
        workout_id = temp_repo.create({"name": "Workout1", "duration": 30}, type_="workout")
        
        args = Mock()
        args.user_id = user_id
        args.workout_id = workout_id
        args.strategy = None
        
        cli_schedule(args)
        
        captured = capsys.readouterr()
        assert "scheduled" in captured.out.lower()

    def test_cli_schedule_simple_strategy(self, temp_repo, capsys):
        user_id = temp_repo.create({"username": "User1", "age": 25, "weight": 70.0}, type_="user")
        workout_id = temp_repo.create({"name": "Workout1", "duration": 30}, type_="workout")
        
        args = Mock()
        args.user_id = user_id
        args.workout_id = workout_id
        args.strategy = "simple"
        args.met = 6.0
        
        cli_schedule(args)
        
        captured = capsys.readouterr()
        assert "scheduled" in captured.out.lower()
        assert "calories" in captured.out.lower()

    def test_cli_schedule_constant_strategy(self, temp_repo, capsys):
        user_id = temp_repo.create({"username": "User1", "age": 25}, type_="user")
        workout_id = temp_repo.create({"name": "Workout1", "duration": 30}, type_="workout")
        
        args = Mock()
        args.user_id = user_id
        args.workout_id = workout_id
        args.strategy = "constant"
        args.rate_per_min = 5.0
        
        cli_schedule(args)
        
        captured = capsys.readouterr()
        assert "scheduled" in captured.out.lower()

    def test_cli_schedule_user_not_found(self, temp_repo, capsys):
        workout_id = temp_repo.create({"name": "Workout1", "duration": 30}, type_="workout")
        
        args = Mock()
        args.user_id = "nonexistent"
        args.workout_id = workout_id
        args.strategy = None
        
        cli_schedule(args)
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_cli_schedule_workout_not_found(self, temp_repo, capsys):
        user_id = temp_repo.create({"username": "User1", "age": 25}, type_="user")
        
        args = Mock()
        args.user_id = user_id
        args.workout_id = "nonexistent"
        args.strategy = None
        
        cli_schedule(args)
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()
