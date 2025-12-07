import logging
from repository.repository import Repository

logger = logging.getLogger(__name__)


class WorkoutService:
    """High-level workout operations that wrap the Repository."""

    def __init__(self, repo: Repository = None):
        self.repo = repo or Repository()

    def create_workout(self, name: str, duration: int):
        """Create a new workout record."""
        try:
            if not name or not isinstance(name, str):
                raise ValueError("Workout name must be a non-empty string")
            if not isinstance(duration, int) or duration <= 0:
                raise ValueError("Duration must be a positive integer")
            
            data = {"name": name, "duration": duration}
            record_id = self.repo.create(data, type_="workout")
            logger.info("Created workout: %s (id=%s)", name, record_id)
            return record_id
        except ValueError as e:
            logger.error("Validation error creating workout: %s", e)
            raise
        except Exception as e:
            logger.exception("Failed to create workout: %s", e)
            raise

    def update_workout(self, record_id: str, name: str = None, duration: int = None):
        """Update an existing workout record."""
        try:
            record = self.repo.read_by_id(record_id)
            if not record:
                raise ValueError(f"Workout with id={record_id} not found")
            
            if record.get("type") != "workout":
                raise ValueError(f"Record {record_id} is not a workout")
            
            data = record.get("data", {})
            
            if name is not None:
                if not name or not isinstance(name, str):
                    raise ValueError("Workout name must be a non-empty string")
                data["name"] = name
            
            if duration is not None:
                if not isinstance(duration, int) or duration <= 0:
                    raise ValueError("Duration must be a positive integer")
                data["duration"] = duration
            
            success = self.repo.update(record_id, data)
            if success:
                logger.info("Updated workout id=%s", record_id)
            return success
        except ValueError as e:
            logger.error("Validation error updating workout: %s", e)
            raise
        except Exception as e:
            logger.exception("Failed to update workout id=%s: %s", record_id, e)
            raise

    def delete_workout(self, record_id: str):
        """Delete a workout record."""
        try:
            record = self.repo.read_by_id(record_id)
            if not record:
                raise ValueError(f"Workout with id={record_id} not found")
            
            if record.get("type") != "workout":
                raise ValueError(f"Record {record_id} is not a workout")
            
            success = self.repo.delete(record_id)
            if success:
                logger.info("Deleted workout id=%s", record_id)
            return success
        except ValueError as e:
            logger.error("Error deleting workout: %s", e)
            raise
        except Exception as e:
            logger.exception("Failed to delete workout id=%s: %s", record_id, e)
            raise

    def list_workouts(self):
        """List only workout records."""
        try:
            return self.repo.find_by_type("workout")
        except Exception as e:
            logger.exception("Failed to list workouts: %s", e)
            raise

    def read_record(self, record_id: str):
        """Read a record by ID."""
        return self.repo.read_by_id(record_id)

    def get_domain_by_id(self, record_id: str):
        """Get domain object by ID."""
        return self.repo.get_object_by_id(record_id)
