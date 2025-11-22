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


def test_factory_create_from_record():
    from models.factory import ObjectFactory

    record = {"id": "1", "type": "user", "data": {"username": "dave", "age": 40}}
    obj = ObjectFactory.create_from_record(record)
    assert isinstance(obj, User)
    assert obj.username == "dave"
    assert obj.age == 40


def test_repository_read_write_tmpfile(tmp_path):
    temp_file = tmp_path / "temp_data.json"
    repo = Repository(str(temp_file))
    # Should start empty
    assert repo.read_all() == []
    # Create a structured record and validate returned id
    item = {"username": "carl", "age": 20}
    record_id = repo.create(item, type_="user")
    assert isinstance(record_id, str) and len(record_id) > 0

    # read_by_id should return the record
    read = repo.read_by_id(record_id)
    assert read is not None
    assert read.get("id") == record_id
    assert read.get("type") == "user"
    assert read.get("data").get("username") == "carl"

    # update should replace data
    updated = repo.update(record_id, {"username": "carl", "age": 21})
    assert updated is True
    assert repo.read_by_id(record_id).get("data").get("age") == 21

    # delete should remove record
    deleted = repo.delete(record_id)
    assert deleted is True
    assert repo.read_by_id(record_id) is None


def test_repository_get_object_by_id(tmp_path):
    temp_file = tmp_path / "temp_data.json"
    repo = Repository(str(temp_file))
    item = {"username": "ellen", "age": 28}
    record_id = repo.create(item, type_="user")

    obj = repo.get_object_by_id(record_id)
    assert obj is not None
    assert isinstance(obj, User)
    assert obj.username == "ellen"
