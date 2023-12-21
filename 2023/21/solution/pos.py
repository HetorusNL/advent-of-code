class Pos:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def hash(self):
        return f"{self.row},{self.col}"
