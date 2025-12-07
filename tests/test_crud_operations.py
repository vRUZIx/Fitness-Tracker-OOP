import pytest
from services.user_service import UserService
from services.workout_service import WorkoutService
from repository.repository import Repository
import tempfile
import os


@pytest.fixture
def temp_repo():
    """Create a temporary repository for testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    repo = Repository(filename=path)
    yield repo
    os.unlink(path)


class TestUserServiceCRUD:
    """Test complete CRUD operations for UserService."""

    def test_create_user_success(self, temp_repo):
        service = UserService(repo=temp_repo)
        user_id = service.create_user("Alice", 25, height=165.0, weight=60.0)
        assert user_id is not None
        record = service.read_record(user_id)
        assert record["type"] == "user"
        assert record["data"]["username"] == "Alice"
        assert record["data"]["age"] == 25

    def test_create_user_validation(self, temp_repo):
        service = UserService(repo=temp_repo)
        with pytest.raises(ValueError, match="Username must be a non-empty string"):
            service.create_user("", 25)
        with pytest.raises(ValueError, match="Age must be a positive integer"):
            service.create_user("Bob", -5)

    def test_update_user_success(self, temp_repo):
        service = UserService(repo=temp_repo)
        user_id = service.create_user("Charlie", 30, height=170.0, weight=70.0)
        success = service.update_user(user_id, username="Charles", age=31)
        assert success is True
        record = service.read_record(user_id)
        assert record["data"]["username"] == "Charles"
        assert record["data"]["age"] == 31
        assert record["data"]["height"] == 170.0

    def test_update_user_not_found(self, temp_repo):
        service = UserService(repo=temp_repo)
        with pytest.raises(ValueError, match="not found"):
            service.update_user("nonexistent_id", username="Test")

    def test_update_user_partial(self, temp_repo):
        service = UserService(repo=temp_repo)
        user_id = service.create_user("Dave", 40, height=180.0, weight=80.0)
        service.update_user(user_id, weight=75.0)
        record = service.read_record(user_id)
        assert record["data"]["username"] == "Dave"
        assert record["data"]["age"] == 40
        assert record["data"]["weight"] == 75.0

    def test_delete_user_success(self, temp_repo):
        service = UserService(repo=temp_repo)
        user_id = service.create_user("Eve", 28)
        success = service.delete_user(user_id)
        assert success is True
        record = service.read_record(user_id)
        assert record is None

    def test_delete_user_not_found(self, temp_repo):
        service = UserService(repo=temp_repo)
        with pytest.raises(ValueError, match="not found"):
            service.delete_user("nonexistent_id")

    def test_list_users(self, temp_repo):
        service = UserService(repo=temp_repo)
        service.create_user("User1", 20)
        service.create_user("User2", 30)
        service.create_user("User3", 40)
        users = service.list_users()
        assert len(users) == 3
        assert all(u["type"] == "user" for u in users)


class TestWorkoutServiceCRUD:
    """Test complete CRUD operations for WorkoutService."""

    def test_create_workout_success(self, temp_repo):
        service = WorkoutService(repo=temp_repo)
        workout_id = service.create_workout("Morning Run", 30)
        assert workout_id is not None
        record = service.read_record(workout_id)
        assert record["type"] == "workout"
        assert record["data"]["name"] == "Morning Run"
        assert record["data"]["duration"] == 30

    def test_create_workout_validation(self, temp_repo):
        service = WorkoutService(repo=temp_repo)
        with pytest.raises(ValueError, match="Workout name must be a non-empty string"):
            service.create_workout("", 30)
        with pytest.raises(ValueError, match="Duration must be a positive integer"):
            service.create_workout("Test", -10)

    def test_update_workout_success(self, temp_repo):
        service = WorkoutService(repo=temp_repo)
        workout_id = service.create_workout("Evening Walk", 20)
        success = service.update_workout(workout_id, name="Evening Jog", duration=25)
        assert success is True
        record = service.read_record(workout_id)
        assert record["data"]["name"] == "Evening Jog"
        assert record["data"]["duration"] == 25

    def test_update_workout_not_found(self, temp_repo):
        service = WorkoutService(repo=temp_repo)
        with pytest.raises(ValueError, match="not found"):
            service.update_workout("nonexistent_id", name="Test")

    def test_update_workout_partial(self, temp_repo):
        service = WorkoutService(repo=temp_repo)
        workout_id = service.create_workout("Yoga", 45)
        service.update_workout(workout_id, duration=60)
        record = service.read_record(workout_id)
        assert record["data"]["name"] == "Yoga"
        assert record["data"]["duration"] == 60

    def test_delete_workout_success(self, temp_repo):
        service = WorkoutService(repo=temp_repo)
        workout_id = service.create_workout("Swimming", 40)
        success = service.delete_workout(workout_id)
        assert success is True
        record = service.read_record(workout_id)
        assert record is None

    def test_delete_workout_not_found(self, temp_repo):
        service = WorkoutService(repo=temp_repo)
        with pytest.raises(ValueError, match="not found"):
            service.delete_workout("nonexistent_id")

    def test_list_workouts(self, temp_repo):
        service = WorkoutService(repo=temp_repo)
        service.create_workout("Workout1", 20)
        service.create_workout("Workout2", 30)
        service.create_workout("Workout3", 40)
        workouts = service.list_workouts()
        assert len(workouts) == 3
        assert all(w["type"] == "workout" for w in workouts)


class TestCRUDEdgeCases:
    """Test edge cases for CRUD operations."""

    def test_update_wrong_type(self, temp_repo):
        user_service = UserService(repo=temp_repo)
        workout_service = WorkoutService(repo=temp_repo)
        workout_id = workout_service.create_workout("Test", 30)
        with pytest.raises(ValueError, match="is not a user"):
            user_service.update_user(workout_id, username="Test")

    def test_delete_wrong_type(self, temp_repo):
        user_service = UserService(repo=temp_repo)
        workout_service = WorkoutService(repo=temp_repo)
        user_id = user_service.create_user("Test", 25)
        with pytest.raises(ValueError, match="is not a workout"):
            workout_service.delete_workout(user_id)

    def test_mixed_records_filtering(self, temp_repo):
        user_service = UserService(repo=temp_repo)
        workout_service = WorkoutService(repo=temp_repo)
        user_service.create_user("User1", 25)
        workout_service.create_workout("Workout1", 30)
        user_service.create_user("User2", 30)
        workout_service.create_workout("Workout2", 40)
        
        users = user_service.list_users()
        workouts = workout_service.list_workouts()
        
        assert len(users) == 2
        assert len(workouts) == 2
