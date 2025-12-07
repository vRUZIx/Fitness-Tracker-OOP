import json
import os
import pytest

from repository.repository import Repository


def test_read_handles_corrupt_json(tmp_path):
    temp_file = tmp_path / "bad.json"
    # write invalid JSON
    temp_file.write_text("{ not valid json")

    repo = Repository(str(temp_file))
    # read_all should return empty list when JSON is invalid
    assert repo.read_all() == []


def test_find_by_type_returns_matching_records(tmp_path):
    temp_file = tmp_path / "data.json"
    repo = Repository(str(temp_file))

    id1 = repo.create({"username": "a"}, type_="user")
    id2 = repo.create({"username": "b"}, type_="user")
    id3 = repo.create({"name": "run"}, type_="workout")

    users = repo.find_by_type("user")
    assert isinstance(users, list)
    assert any(r["id"] == id1 for r in users)
    assert any(r["id"] == id2 for r in users)
    assert all(r["type"] == "user" for r in users)


def test_create_propagates_write_exceptions(monkeypatch, tmp_path):
    temp_file = tmp_path / "data.json"
    repo = Repository(str(temp_file))

    # monkeypatch the _write method to raise an IOError
    def fail_write(data):
        raise IOError("disk full")

    monkeypatch.setattr(repo, "_write", fail_write)

    with pytest.raises(IOError):
        repo.create({"username": "fail"}, type_="user")
