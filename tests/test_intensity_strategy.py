import pytest
from strategies.intensity_strategy import AgeBasedIntensityStrategy, DurationBasedIntensityStrategy
from models.user import User
from models.workout import Workout


class TestAgeBasedIntensityStrategy:
    """Test age-based intensity calculation strategy."""

    def test_young_user_short_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Alice", 25, height=165.0, weight=60.0)
        workout = Workout("Quick Run", 20)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Moderate"

    def test_young_user_medium_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Bob", 28, height=170.0, weight=70.0)
        workout = Workout("Cardio", 45)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "High"

    def test_young_user_long_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Charlie", 29, height=175.0, weight=75.0)
        workout = Workout("Marathon", 90)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Very High"

    def test_middle_age_user_short_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Dave", 40, height=180.0, weight=80.0)
        workout = Workout("Walk", 25)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Low"

    def test_middle_age_user_medium_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Eve", 45, height=160.0, weight=65.0)
        workout = Workout("Cycling", 50)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Moderate"

    def test_middle_age_user_long_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Frank", 49, height=178.0, weight=85.0)
        workout = Workout("Hiking", 70)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "High"

    def test_senior_user_short_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Grace", 60, height=165.0, weight=70.0)
        workout = Workout("Stretching", 20)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Low"

    def test_senior_user_medium_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Henry", 55, height=172.0, weight=78.0)
        workout = Workout("Swimming", 40)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Moderate"

    def test_senior_user_long_workout(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Iris", 65, height=158.0, weight=68.0)
        workout = Workout("Long Walk", 50)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "High"

    def test_missing_age(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Test", None)
        workout = Workout("Test", 30)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Unknown"

    def test_missing_duration(self):
        strategy = AgeBasedIntensityStrategy()
        user = User("Test", 30)
        workout = Workout("Test", None)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Unknown"


class TestDurationBasedIntensityStrategy:
    """Test duration-based intensity calculation strategy."""

    def test_light_workout(self):
        strategy = DurationBasedIntensityStrategy()
        user = User("Alice", 25)
        workout = Workout("Quick Exercise", 15)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Light"

    def test_moderate_workout(self):
        strategy = DurationBasedIntensityStrategy()
        user = User("Bob", 30)
        workout = Workout("Regular Exercise", 30)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Moderate"

    def test_high_workout(self):
        strategy = DurationBasedIntensityStrategy()
        user = User("Charlie", 35)
        workout = Workout("Intensive Exercise", 50)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "High"

    def test_intense_workout(self):
        strategy = DurationBasedIntensityStrategy()
        user = User("Dave", 40)
        workout = Workout("Extreme Exercise", 75)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Intense"

    def test_boundary_20_minutes(self):
        strategy = DurationBasedIntensityStrategy()
        user = User("Test", 25)
        workout = Workout("Boundary Test", 20)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Moderate"

    def test_boundary_40_minutes(self):
        strategy = DurationBasedIntensityStrategy()
        user = User("Test", 25)
        workout = Workout("Boundary Test", 40)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "High"

    def test_boundary_60_minutes(self):
        strategy = DurationBasedIntensityStrategy()
        user = User("Test", 25)
        workout = Workout("Boundary Test", 60)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Intense"

    def test_missing_duration(self):
        strategy = DurationBasedIntensityStrategy()
        user = User("Test", 30)
        workout = Workout("Test", None)
        intensity = strategy.calculate_intensity(user, workout)
        assert intensity == "Unknown"
