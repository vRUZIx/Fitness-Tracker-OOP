import logging


logger = logging.getLogger(__name__)


class Scheduler:
    def schedule_workout(self, user, workout):
        # Use public attribute names from User and Workout
        user_name = getattr(user, "username", None) or getattr(user, "_name", "Unknown user")
        workout_name = getattr(workout, "name", None) or getattr(workout, "_title", "Unknown workout")
        logger.info("Scheduling workout '%s' for user '%s'", workout_name, user_name)
        return f"{user_name} scheduled: {workout_name}"