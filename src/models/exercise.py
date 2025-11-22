class Exercise:
    def __init__(self, name, calories):
        self._name = name
        self._calories = calories

    def burn_info(self):
        return f"Exercise: {self._name}, Calories Burned: {self._calories}"