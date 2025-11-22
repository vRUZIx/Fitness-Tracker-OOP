import os
import json
import tempfile
from models.user import User
from models.workout import Workout
from models.exercise import Exercise
from repository.repository import Repository
from services.scheduler import Scheduler


def test_user_get_info_defaults():
    u = User("alice", 30)
    info = u.get_info()
    assert "alice" in info
    assert "N/A" in info


def test_workout_summary():
    w = Workout("Leg Day", 60)
    assert "Leg Day" in w.get_summary()
    assert "60" in w.get_summary()


def test_exercise_burn_info():
    e = Exercise("Pushup", 50)
    assert "Pushup" in e.burn_info()
    assert "50" in e.burn_info()


def test_scheduler_uses_public_attrs():
    u = User("bob", 25)
    w = Workout("Arms", 30)
    s = Scheduler()
    out = s.schedule_workout(u, w)
    assert "bob" in out
    assert "Arms" in out


def test_repository_read_write_tmpfile(tmp_path):
    temp_file = tmp_path / "temp_data.json"
    repo = Repository(str(temp_file))
    # Should start empty
    assert repo.read_all() == []
    item = {"a": 1}
    repo.create(item)
    data = repo.read_all()
    assert isinstance(data, list)
    assert item in data
