import json
from pathlib import Path


class Database:
    def __init__(self, filename: str = "db.json"):
        self.file_name = Path(filename)
        self.create_file()
        self.data = None

    def create_file(self):
        if not self.file_name.exists():
            with open(self.file_name, "w") as f:
                f.write('{"users": {}}')

    def read_database(self) -> dict:
        with open(self.file_name) as f:
            self.data = json.loads(f.read())
        return self.data

    def save_database(self) -> dict:
        with open(self.file_name, "w") as f:
            f.write(json.dumps(self.data, indent=4))

    def add_user(self, user_id: int, first_name: str):
        self.read_database()

        if "users" not in self.data:
            self.data["users"] = {}

        user_id = str(user_id)
        self.data["users"].setdefault(user_id, {"first_name": first_name})

        self.save_database()


db = Database()
