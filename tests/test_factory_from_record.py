import pytest
from models.factory import ObjectFactory
from models.user import User


def test_create_from_record_invalid_type():
    with pytest.raises(ValueError):
        ObjectFactory.create_from_record("not a dict")


def test_create_from_record_unknown_type():
    rec = {"type": "unknown", "data": {}}
    with pytest.raises(ValueError) as exc:
        ObjectFactory.create_from_record(rec)
    assert "Unknown record type" in str(exc.value)


def test_create_from_record_user():
    rec = {"type": "user", "data": {"username": "alice", "age": 30}}
    u = ObjectFactory.create_from_record(rec)
    assert isinstance(u, User)
    assert u.username == "alice"
    assert u.age == 30
