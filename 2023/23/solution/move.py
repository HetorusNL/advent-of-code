from solution.pos import Pos


class Move:
    def __init__(self, to_pos: Pos, length: int):
        self.to_pos = to_pos
        self.length = length

    def __repr__(self):
        return f"{self.length} steps to: {self.to_pos}"
