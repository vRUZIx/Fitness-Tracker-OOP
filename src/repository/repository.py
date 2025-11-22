import json
import os
import uuid
import logging
from .irepository import IRepository

logger = logging.getLogger(__name__)


class Repository(IRepository):
    """JSON file repository storing structured records:
    Each record: {"id": <id>, "type": <type>, "data": <dict>}
    """

    def __init__(self, filename=None):
        # Default to a single data.json at the project root so behavior is deterministic
        if filename is None:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            filename = os.path.join(repo_root, "data.json")

        self.filename = filename
        # Ensure the file exists and contains a JSON array
        if not os.path.exists(self.filename):
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def create(self, item_dict: dict, type_: str = None) -> str:
        logger.info("Creating record of type=%s", type_)
        records = self._read()
        # If incoming item already looks like a full record, accept it
        if "id" in item_dict and "data" in item_dict:
            record = item_dict
        else:
            record = {
                "id": uuid.uuid4().hex,
                "type": type_ or item_dict.get("type") or "generic",
                "data": item_dict,
            }

        records.append(record)
        try:
            self._write(records)
        except Exception:
            logger.exception("Failed to write record to %s", self.filename)
            raise
        logger.debug("Created record id=%s", record["id"])
        return record["id"]

    def read_all(self) -> list:
        logger.debug("Reading all records from %s", self.filename)
        return self._read()

    def read_by_id(self, record_id: str) -> dict:
        logger.debug("Reading record by id=%s", record_id)
        records = self._read()
        for r in records:
            if r.get("id") == record_id:
                return r
        logger.debug("Record id=%s not found", record_id)
        return None

    def update(self, record_id: str, new_data: dict) -> bool:
        logger.info("Updating record id=%s", record_id)
        records = self._read()
        updated = False
        for r in records:
            if r.get("id") == record_id:
                r["data"] = new_data
                updated = True
                break
        if updated:
            try:
                self._write(records)
            except Exception:
                logger.exception("Failed to write updated records to %s", self.filename)
                raise
            logger.debug("Updated record id=%s", record_id)
        else:
            logger.debug("No record updated for id=%s", record_id)
        return updated

    def delete(self, record_id: str) -> bool:
        logger.info("Deleting record id=%s", record_id)
        records = self._read()
        before = len(records)
        records = [r for r in records if r.get("id") != record_id]
        after = len(records)
        if after < before:
            try:
                self._write(records)
            except Exception:
                logger.exception("Failed to write records after delete to %s", self.filename)
                raise
            logger.debug("Deleted record id=%s", record_id)
            return True
        logger.debug("No record deleted for id=%s", record_id)
        return False

    def find_by_type(self, type_: str) -> list:
        records = self._read()
        return [r for r in records if r.get("type") == type_]

    def _read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is empty/corrupt or missing, return empty list
            logger.warning("Returning empty record list for file %s (missing or invalid JSON)", self.filename)
            return []

    def _write(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.debug("Wrote %d records to %s", len(data), self.filename)

    def get_object_by_id(self, record_id: str):
        """Return a domain object created by the factory for the record id, or None."""
        record = self.read_by_id(record_id)
        if not record:
            return None

        try:
            # Import here to avoid top-level circular imports
            from models.factory import ObjectFactory

            return ObjectFactory.create_from_record(record)
        except Exception:
            logger.exception("Failed to build domain object from record id=%s", record_id)
            return None