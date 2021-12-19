from typing import Union


class Coord:
    def __init__(self, inp: Union[str, list, None] = None):
        if isinstance(inp, str):
            self.x, self.y, self.z = [int(num) for num in inp.split(",")]
        elif isinstance(inp, list):
            self.x, self.y, self.z = inp
        else:
            self.x = 0
            self.y = 0
            self.z = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def values(self):
        return [self.x, self.y, self.z]

    def __add__(self, other):
        return Coord([self.x + other.x, self.y + other.y, self.z + other.z])

    def __sub__(self, other):
        return Coord([self.x - other.x, self.y - other.y, self.z - other.z])
