import pytest

from models.factory import ObjectFactory
from strategies.calorie_strategy import SimpleCalorieStrategy, ConstantBurnStrategy, get_strategy
from services.scheduler import Scheduler


def test_simple_calorie_strategy():
    user = ObjectFactory.create_object("user", "bob", 28, weight=70)
    workout = ObjectFactory.create_object("workout", "Run", 30)
    strat = SimpleCalorieStrategy(met=6.0)
    calories = strat.calculate(user, workout)
    # expected: 70 * 30 * 0.0175 * 6 = 220.5
    assert pytest.approx(calories, rel=1e-3) == 220.5


def test_constant_burn_strategy():
    user = ObjectFactory.create_object("user", "bob", 28, weight=70)
    workout = ObjectFactory.create_object("workout", "Walk", 20)
    strat = ConstantBurnStrategy(rate_per_min=4.0)
    calories = strat.calculate(user, workout)
    assert calories == 80.0


def test_get_strategy_factory():
    s = get_strategy("simple", met=5.0)
    assert isinstance(s, SimpleCalorieStrategy)
    s2 = get_strategy("constant", rate_per_min=3.0)
    assert isinstance(s2, ConstantBurnStrategy)


def test_scheduler_uses_strategy():
    user = ObjectFactory.create_object("user", "alice", 30, weight=60)
    workout = ObjectFactory.create_object("workout", "Yoga", 45)
    scheduler = Scheduler()
    msg = scheduler.schedule_workout(user, workout, strategy=SimpleCalorieStrategy(met=3.0))
    assert "Estimated calories" in msg
