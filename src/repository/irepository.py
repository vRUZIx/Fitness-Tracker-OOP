from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def create(self, item_dict: dict, type_: str = None) -> str:
        """Create a new record and return its id."""

    @abstractmethod
    def read_all(self) -> list:
        """Return all records as a list."""

    @abstractmethod
    def read_by_id(self, record_id: str) -> dict:
        """Return a single record by id or None."""

    @abstractmethod
    def update(self, record_id: str, new_data: dict) -> bool:
        """Update record data by id. Return True if updated."""

    @abstractmethod
    def delete(self, record_id: str) -> bool:
        """Delete a record by id. Return True if deleted."""

    @abstractmethod
    def find_by_type(self, type_: str) -> list:
        """Return records matching the provided type."""
