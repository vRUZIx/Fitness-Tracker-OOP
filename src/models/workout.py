class Workout:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def get_summary(self):
        return f"Workout: {self.name}, Duration: {self.duration} minutes"
