import pytest

from models.factory import ObjectFactory
from models.user import User
from models.workout import Workout
from logging_config import configure_logging


def test_create_object_with_kwargs():
    u = ObjectFactory.create_object("user", username="sam", age=29)
    assert isinstance(u, User)
    assert u.username == "sam"
    assert u.age == 29


def test_create_from_record_unknown_type_raises():
    record = {"id": "x", "type": "unknown", "data": {}}
    with pytest.raises(ValueError):
        ObjectFactory.create_from_record(record)


def test_configure_logging_returns_logger():
    logger = configure_logging()
    assert logger is not None
    # logger should have a name attribute
    assert hasattr(logger, "name")
