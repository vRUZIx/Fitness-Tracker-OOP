from abc import ABC, abstractmethod


class IntensityStrategy(ABC):
    """Abstract strategy for determining workout intensity levels."""

    @abstractmethod
    def calculate_intensity(self, user, workout) -> str:
        """Calculate workout intensity based on user attributes and workout details."""


class AgeBasedIntensityStrategy(IntensityStrategy):
    """Determines intensity based on user's age and workout duration."""

    def calculate_intensity(self, user, workout) -> str:
        age = getattr(user, "age", None)
        duration = getattr(workout, "duration", None)
        
        if age is None or duration is None:
            return "Unknown"
        
        if age < 30:
            if duration < 30:
                return "Moderate"
            elif duration < 60:
                return "High"
            else:
                return "Very High"
        elif age < 50:
            if duration < 30:
                return "Low"
            elif duration < 60:
                return "Moderate"
            else:
                return "High"
        else:
            if duration < 30:
                return "Low"
            elif duration < 45:
                return "Moderate"
            else:
                return "High"


class DurationBasedIntensityStrategy(IntensityStrategy):
    """Determines intensity purely based on workout duration."""

    def calculate_intensity(self, user, workout) -> str:
        duration = getattr(workout, "duration", None)
        
        if duration is None:
            return "Unknown"
        
        if duration < 20:
            return "Light"
        elif duration < 40:
            return "Moderate"
        elif duration < 60:
            return "High"
        else:
            return "Intense"
