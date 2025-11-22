from .user import User
from .workout import Workout
from .exercise import Exercise


class ObjectFactory:
    @staticmethod
    def create_object(object_type, *args, **kwargs):
        """Create an object by type using positional or keyword args.

        Examples:
            create_object('user', 'alice', 30)
            create_object('user', username='alice', age=30)
        """
        if object_type == "user":
            return User(*args, **kwargs)
        elif object_type == "workout":
            return Workout(*args, **kwargs)
        elif object_type == "exercise":
            return Exercise(*args, **kwargs)
        else:
            raise ValueError("Unknown object type")

    @staticmethod
    def create_from_record(record: dict):
        """Create a domain object from a structured record.

        The record is expected to have keys: 'type' and 'data', where 'data'
        is a dict of fields matching the model constructor.
        """
        if not isinstance(record, dict):
            raise ValueError("record must be a dict")

        rec_type = record.get("type")
        data = record.get("data") or {}

        if rec_type == "user":
            return User(**data)
        elif rec_type == "workout":
            return Workout(**data)
        elif rec_type == "exercise":
            return Exercise(**data)
        else:
            raise ValueError(f"Unknown record type: {rec_type}")