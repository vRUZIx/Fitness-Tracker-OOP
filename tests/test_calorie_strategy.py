import pytest
from models.user import User
from models.workout import Workout
from strategies.calorie_strategy import (
    SimpleCalorieStrategy,
    ConstantBurnStrategy,
    get_strategy,
)


def test_get_strategy_errors():
    with pytest.raises(ValueError):
        get_strategy(None)

    with pytest.raises(ValueError):
        get_strategy("unknown")


def test_simple_strategy_requires_weight():
    s = SimpleCalorieStrategy()
    user = User("bob", 25)  # weight is None
    workout = Workout("run", 30)
    with pytest.raises(ValueError):
        s.calculate(user, workout)


def test_simple_strategy_calculation():
    s = SimpleCalorieStrategy(met=6.0)
    user = User("bob", 25, weight=70)
    workout = Workout("run", 60)
    assert pytest.approx(441.0) == s.calculate(user, workout)


def test_constant_strategy_requires_duration():
    c = ConstantBurnStrategy(rate_per_min=4.0)
    user = User("bob", 25, weight=70)
    workout = type("W", (object,), {})()  # no duration attribute
    with pytest.raises(ValueError):
        c.calculate(user, workout)


def test_constant_strategy_calculation():
    c = ConstantBurnStrategy(rate_per_min=4.0)
    workout = Workout("yoga", 30)
    user = User("bob", 25, weight=70)
    assert c.calculate(user, workout) == 120.0
