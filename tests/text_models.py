from src.models.user import User
from src.models.exercise import Exercise


def test_user_info():
    u = User("Test", 20)
    assert u.get_info() == "User: Test, Age: 20"


def test_exercise_burn():
    e = Exercise("Running", 300)
    assert e.burn_info() == "Exercise: Running, Calories Burned: 300"