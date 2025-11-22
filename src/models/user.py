class User:
    def __init__(self, username, age, height=None, weight=None):
        self.username = username
        self.age = age
        self.height = height
        self.weight = weight

    def to_dict(self):
        return {
            "username": self.username,
            "age": self.age,
            "height": self.height,
            "weight": self.weight
        }

    def get_info(self):
        h = self.height if self.height is not None else "N/A"
        w = self.weight if self.weight is not None else "N/A"
        return f"User: {self.username}, Age: {self.age}, Height: {h}, Weight: {w}"
