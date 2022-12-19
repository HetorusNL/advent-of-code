from copy import deepcopy

from solution.rock import Rock


class Rocks:
    def __init__(self):
        self._rock_positions: list[list[list[int]]] = [
            # the - rock
            [[0, 0], [1, 0], [2, 0], [3, 0]],
            # the + rock
            [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]],
            # the inverted L rock
            [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]],
            # the | rock
            [[0, 0], [0, 1], [0, 2], [0, 3]],
            # the square rock
            [[0, 0], [1, 0], [0, 1], [1, 1]],
        ]
        self._next_rock: int = 0

    def get_rock(self) -> Rock:
        rock = Rock(deepcopy(self._rock_positions[self._next_rock]))
        self._next_rock = (self._next_rock + 1) % len(self._rock_positions)
        return rock

    @property
    def num_different_rocks(self) -> int:
        return len(self._rock_positions)
