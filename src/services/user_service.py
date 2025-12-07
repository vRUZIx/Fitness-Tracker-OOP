import logging
from repository.repository import Repository

logger = logging.getLogger(__name__)


class UserService:
    """High-level user operations that wrap the Repository and factory usage.

    This keeps CLI and business logic separated.
    """

    def __init__(self, repo: Repository = None):
        self.repo = repo or Repository()

    def create_user(self, username: str, age: int, height: float = None, weight: float = None):
        """Create a new user record."""
        try:
            if not username or not isinstance(username, str):
                raise ValueError("Username must be a non-empty string")
            if not isinstance(age, int) or age <= 0:
                raise ValueError("Age must be a positive integer")
            
            data = {"username": username, "age": age}
            if height is not None:
                if not isinstance(height, (int, float)) or height <= 0:
                    raise ValueError("Height must be a positive number")
                data["height"] = height
            if weight is not None:
                if not isinstance(weight, (int, float)) or weight <= 0:
                    raise ValueError("Weight must be a positive number")
                data["weight"] = weight
            
            record_id = self.repo.create(data, type_="user")
            logger.info("Created user: %s (id=%s)", username, record_id)
            return record_id
        except ValueError as e:
            logger.error("Validation error creating user: %s", e)
            raise
        except Exception as e:
            logger.exception("Failed to create user: %s", e)
            raise

    def update_user(self, record_id: str, username: str = None, age: int = None, height: float = None, weight: float = None):
        """Update an existing user record."""
        try:
            record = self.repo.read_by_id(record_id)
            if not record:
                raise ValueError(f"User with id={record_id} not found")
            
            if record.get("type") != "user":
                raise ValueError(f"Record {record_id} is not a user")
            
            data = record.get("data", {})
            
            if username is not None:
                if not username or not isinstance(username, str):
                    raise ValueError("Username must be a non-empty string")
                data["username"] = username
            
            if age is not None:
                if not isinstance(age, int) or age <= 0:
                    raise ValueError("Age must be a positive integer")
                data["age"] = age
            
            if height is not None:
                if not isinstance(height, (int, float)) or height <= 0:
                    raise ValueError("Height must be a positive number")
                data["height"] = height
            
            if weight is not None:
                if not isinstance(weight, (int, float)) or weight <= 0:
                    raise ValueError("Weight must be a positive number")
                data["weight"] = weight
            
            success = self.repo.update(record_id, data)
            if success:
                logger.info("Updated user id=%s", record_id)
            return success
        except ValueError as e:
            logger.error("Validation error updating user: %s", e)
            raise
        except Exception as e:
            logger.exception("Failed to update user id=%s: %s", record_id, e)
            raise

    def delete_user(self, record_id: str):
        """Delete a user record."""
        try:
            record = self.repo.read_by_id(record_id)
            if not record:
                raise ValueError(f"User with id={record_id} not found")
            
            if record.get("type") != "user":
                raise ValueError(f"Record {record_id} is not a user")
            
            success = self.repo.delete(record_id)
            if success:
                logger.info("Deleted user id=%s", record_id)
            return success
        except ValueError as e:
            logger.error("Error deleting user: %s", e)
            raise
        except Exception as e:
            logger.exception("Failed to delete user id=%s: %s", record_id, e)
            raise

    def list_all(self):
        """List all records."""
        return self.repo.read_all()

    def list_users(self):
        """List only user records."""
        try:
            return self.repo.find_by_type("user")
        except Exception as e:
            logger.exception("Failed to list users: %s", e)
            raise

    def read_record(self, record_id: str):
        """Read a record by ID."""
        return self.repo.read_by_id(record_id)

    def get_domain_by_id(self, record_id: str):
        """Get domain object by ID."""
        return self.repo.get_object_by_id(record_id)
