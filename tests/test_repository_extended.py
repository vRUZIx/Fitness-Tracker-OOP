import pytest
from repository.repository import Repository
import tempfile
import os
import json


@pytest.fixture
def temp_repo():
    """Create a temporary repository for testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    repo = Repository(filename=path)
    yield repo
    os.unlink(path)


class TestRepositoryEdgeCases:
    """Extended edge case testing for Repository."""

    def test_create_with_special_characters(self, temp_repo):
        data = {"name": "Test@#$%^&*()", "value": 123}
        record_id = temp_repo.create(data, type_="test")
        assert record_id is not None
        record = temp_repo.read_by_id(record_id)
        assert record["data"]["name"] == "Test@#$%^&*()"

    def test_create_with_unicode(self, temp_repo):
        data = {"name": "Тест", "emoji": "🏃‍♂️"}
        record_id = temp_repo.create(data, type_="test")
        record = temp_repo.read_by_id(record_id)
        assert record["data"]["name"] == "Тест"
        assert record["data"]["emoji"] == "🏃‍♂️"

    def test_update_nonexistent_record(self, temp_repo):
        success = temp_repo.update("nonexistent_id", {"data": "test"})
        assert success is False

    def test_delete_nonexistent_record(self, temp_repo):
        success = temp_repo.delete("nonexistent_id")
        assert success is False

    def test_multiple_deletes(self, temp_repo):
        record_id = temp_repo.create({"test": "data"}, type_="test")
        assert temp_repo.delete(record_id) is True
        assert temp_repo.delete(record_id) is False

    def test_update_preserves_id_and_type(self, temp_repo):
        record_id = temp_repo.create({"name": "Original"}, type_="test")
        temp_repo.update(record_id, {"name": "Updated"})
        record = temp_repo.read_by_id(record_id)
        assert record["id"] == record_id
        assert record["type"] == "test"
        assert record["data"]["name"] == "Updated"

    def test_concurrent_operations(self, temp_repo):
        ids = []
        for i in range(10):
            record_id = temp_repo.create({"index": i}, type_="test")
            ids.append(record_id)
        
        records = temp_repo.read_all()
        assert len(records) == 10
        
        for i, record_id in enumerate(ids):
            temp_repo.update(record_id, {"index": i * 2})
        
        for i, record_id in enumerate(ids):
            record = temp_repo.read_by_id(record_id)
            assert record["data"]["index"] == i * 2

    def test_empty_data(self, temp_repo):
        record_id = temp_repo.create({}, type_="empty")
        record = temp_repo.read_by_id(record_id)
        assert record["data"] == {}

    def test_nested_data_structures(self, temp_repo):
        data = {
            "user": {
                "name": "Test",
                "metadata": {
                    "created": "2025-01-01",
                    "tags": ["fitness", "health"]
                }
            }
        }
        record_id = temp_repo.create(data, type_="complex")
        record = temp_repo.read_by_id(record_id)
        assert record["data"]["user"]["metadata"]["tags"] == ["fitness", "health"]

    def test_large_dataset(self, temp_repo):
        for i in range(100):
            temp_repo.create({"index": i, "data": f"Item {i}"}, type_="bulk")
        
        records = temp_repo.read_all()
        assert len(records) == 100
        
        bulk_records = temp_repo.find_by_type("bulk")
        assert len(bulk_records) == 100

    def test_file_persistence(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        
        try:
            repo1 = Repository(filename=path)
            record_id = repo1.create({"test": "data"}, type_="test")
            
            repo2 = Repository(filename=path)
            record = repo2.read_by_id(record_id)
            assert record is not None
            assert record["data"]["test"] == "data"
        finally:
            os.unlink(path)

    def test_find_by_type_empty(self, temp_repo):
        records = temp_repo.find_by_type("nonexistent")
        assert records == []

    def test_read_by_id_none(self, temp_repo):
        record = temp_repo.read_by_id(None)
        assert record is None


class TestRepositoryDataIntegrity:
    """Test data integrity in Repository operations."""

    def test_update_does_not_affect_other_records(self, temp_repo):
        id1 = temp_repo.create({"name": "Record1"}, type_="test")
        id2 = temp_repo.create({"name": "Record2"}, type_="test")
        
        temp_repo.update(id1, {"name": "Updated1"})
        
        record2 = temp_repo.read_by_id(id2)
        assert record2["data"]["name"] == "Record2"

    def test_delete_does_not_affect_other_records(self, temp_repo):
        id1 = temp_repo.create({"name": "Record1"}, type_="test")
        id2 = temp_repo.create({"name": "Record2"}, type_="test")
        id3 = temp_repo.create({"name": "Record3"}, type_="test")
        
        temp_repo.delete(id2)
        
        assert temp_repo.read_by_id(id1) is not None
        assert temp_repo.read_by_id(id2) is None
        assert temp_repo.read_by_id(id3) is not None

    def test_type_filtering_accuracy(self, temp_repo):
        temp_repo.create({"name": "User1"}, type_="user")
        temp_repo.create({"name": "Workout1"}, type_="workout")
        temp_repo.create({"name": "User2"}, type_="user")
        temp_repo.create({"name": "Workout2"}, type_="workout")
        temp_repo.create({"name": "Exercise1"}, type_="exercise")
        
        users = temp_repo.find_by_type("user")
        workouts = temp_repo.find_by_type("workout")
        exercises = temp_repo.find_by_type("exercise")
        
        assert len(users) == 2
        assert len(workouts) == 2
        assert len(exercises) == 1
