import logging
from typing import Optional, Union

from strategies.calorie_strategy import CalorieStrategy, get_strategy


logger = logging.getLogger(__name__)


class Scheduler:
    def schedule_workout(self, user, workout, strategy: Optional[Union[CalorieStrategy, str]] = None, **strategy_kwargs):
        """Schedule a workout for a user and optionally estimate calories using a strategy.

        `strategy` may be a strategy instance or a string name resolved via `get_strategy`.
        Additional keyword args are forwarded to the strategy factory when a string name is supplied.
        """
        # Use public attribute names from User and Workout
        user_name = getattr(user, "username", None) or getattr(user, "_name", "Unknown user")
        workout_name = getattr(workout, "name", None) or getattr(workout, "_title", "Unknown workout")
        logger.info("Scheduling workout '%s' for user '%s'", workout_name, user_name)

        calories_info = None
        try:
            strat_obj = None
            if isinstance(strategy, str):
                strat_obj = get_strategy(strategy, **strategy_kwargs)
            elif isinstance(strategy, CalorieStrategy):
                strat_obj = strategy

            if strat_obj is not None:
                calories = strat_obj.calculate(user, workout)
                calories_info = f" Estimated calories: {calories:.1f} kcal"
        except Exception:
            logger.exception("Calorie strategy failed")

        if calories_info:
            return f"{user_name} scheduled: {workout_name}. {calories_info.strip()}"
        return f"{user_name} scheduled: {workout_name}"