from solution.connection import Connection


class Pos:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def move(self, connection: Connection) -> "Pos":
        return Pos(self.x + connection.x, self.y + connection.y)

    def __eq__(self, other: "Pos"):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f"x{self.x},y{self.y}")

    def __repr__(self):
        return f"[{self.x}, {self.y}]"
