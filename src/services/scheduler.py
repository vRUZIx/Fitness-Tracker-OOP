class Scheduler:
    def schedule_workout(self, user, workout):
        # Use public attribute names from User and Workout
        user_name = getattr(user, "username", None) or getattr(user, "_name", "Unknown user")
        workout_name = getattr(workout, "name", None) or getattr(workout, "_title", "Unknown workout")
        return f"{user_name} scheduled: {workout_name}"