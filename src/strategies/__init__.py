"""Strategy implementations for calorie/burn calculations."""

from .calorie_strategy import (
    CalorieStrategy,
    SimpleCalorieStrategy,
    ConstantBurnStrategy,
    get_strategy,
)

__all__ = [
    "CalorieStrategy",
    "SimpleCalorieStrategy",
    "ConstantBurnStrategy",
    "get_strategy",
]
