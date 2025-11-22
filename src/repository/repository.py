import json
import os


class Repository:
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


    def create(self, item_dict):
        data = self._read()
        data.append(item_dict)
        self._write(data)


    def read_all(self):
        return self._read()


    def _read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is empty/corrupt or missing, return empty list
            return []


    def _write(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)