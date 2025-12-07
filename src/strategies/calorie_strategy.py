from abc import ABC, abstractmethod
from typing import Optional


class CalorieStrategy(ABC):
    """Abstract base for calorie calculation strategies."""

    @abstractmethod
    def calculate(self, user, workout) -> float:
        """Calculate estimated calories burned for the given user and workout."""


class SimpleCalorieStrategy(CalorieStrategy):
    """Simple energy-expenditure calculation using METs.

    Formula: calories = weight_kg * duration_min * 0.0175 * MET
    Default MET is 6.0 (moderate intensity).
    """

    def __init__(self, met: float = 6.0):
        self.met = float(met)

    def calculate(self, user, workout) -> float:
        weight = getattr(user, "weight", None)
        duration = getattr(workout, "duration", None)
        if weight is None or duration is None:
            raise ValueError("User weight and workout duration are required for SimpleCalorieStrategy")
        try:
            return float(weight) * float(duration) * 0.0175 * self.met
        except Exception as e:
            raise ValueError("Failed to calculate calories") from e


class ConstantBurnStrategy(CalorieStrategy):
    """Use a fixed calories-per-minute rate (useful for demonstrations).

    calories = duration_min * rate
    """

    def __init__(self, rate_per_min: float = 5.0):
        self.rate = float(rate_per_min)

    def calculate(self, user, workout) -> float:
        duration = getattr(workout, "duration", None)
        if duration is None:
            raise ValueError("Workout duration required for ConstantBurnStrategy")
        return float(duration) * self.rate


def get_strategy(name: Optional[str], **kwargs) -> CalorieStrategy:
    """Factory helper to get a strategy instance by name.

    Supported names: 'simple', 'constant'
    """
    if not name:
        raise ValueError("Strategy name required")
    n = name.lower()
    if n == "simple":
        return SimpleCalorieStrategy(**kwargs)
    if n == "constant":
        return ConstantBurnStrategy(**kwargs)
    raise ValueError(f"Unknown strategy name: {name}")
