class Pos:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def hash(self):
        return f"{self.row},{self.col}"

    def __repr__(self):
        return self.hash()

    def __eq__(self, other: "Pos"):
        return self.hash() == other.hash()
