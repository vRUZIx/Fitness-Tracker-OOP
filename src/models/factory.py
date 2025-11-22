from .user import User
from .workout import Workout
from .exercise import Exercise


class ObjectFactory:
    @staticmethod
    def create_object(object_type, *args):
        if object_type == "user":
            return User(*args)
        elif object_type == "workout":
            return Workout(*args)
        elif object_type == "exercise":
            return Exercise(*args)
        else:
            raise ValueError("Unknown object type")