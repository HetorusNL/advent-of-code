import re
from typing import Union

from solution.tile import Tile


class Grid3D:
    def __init__(self, lines: list[str]):
        map_regex = re.compile(r"^[.# ]*$")
        path_regex = re.compile(r"^[0-9RL]*$")
        number_regex = re.compile(r"^(?P<number>[0-9]*)")
        direction_regex = re.compile(r"^(?P<direction>[LR])")
        self._grid: dict[int, dict[int, Tile]] = {}
        self._instructions: list[Union[int, str]] = []
        self.FACE_SIZE: int = 50

        for row, line in enumerate(lines):
            if re.match(map_regex, line):
                # parse a grid row and add it to the grid in the form of a line of Tiles
                self._grid[row + 1] = {}
                for col, char in enumerate(line):
                    self._grid[row + 1][col + 1] = Tile(char, row + 1, col + 1)
            elif re.match(path_regex, line):
                # continuously chop of either a number or a direction of line and add to instructions
                while line:
                    if number_match := re.match(number_regex, line):
                        self._instructions.append(int(number_match["number"]))
                        line = line.removeprefix(number_match["number"])
                    if direction_match := re.match(direction_regex, line):
                        self._instructions.append(direction_match["direction"])
                        line = line.removeprefix(direction_match["direction"])

        self._direction: str = "R"  # Up, Down, Left, Right
        row_1_leftmost_col = min(tile.col for tile in self._grid[1].values() if tile.is_open)
        self._current_tile = Tile("T", 1, row_1_leftmost_col)

    def perform_instructions(self) -> None:
        for instruction in self._instructions:
            if type(instruction) is int:
                for _ in range(instruction):
                    if not self._move_performed():
                        break
            elif type(instruction) is str:
                match instruction:
                    case "R":
                        # rotate to the right (clockwise)
                        self._direction = {"R": "D", "D": "L", "L": "U", "U": "R"}[self._direction]
                    case "L":
                        # rotate to the right (clockwise)
                        self._direction = {"R": "U", "U": "L", "L": "D", "D": "R"}[self._direction]

    def _move_performed(self) -> bool:
        tile, direction = self._get_new_tile(self._current_tile.row, self._current_tile.col, self._direction)
        assert tile.is_present, f"issues!"
        if tile.is_open:
            self._current_tile.row = tile.row
            self._current_tile.col = tile.col
            self._direction = direction
            return True
        return False

    def _get_new_tile(self, row: int, col: int, direction: str) -> tuple[Tile, str]:
        # check if we need to wrap (actually if we don't need to wrap, then we can return the tile directly)
        match direction:
            case "R":
                if col % self.FACE_SIZE != 0:
                    return self._grid[row][col + 1], direction
            case "D":
                if row % self.FACE_SIZE != 0:
                    return self._grid[row + 1][col], direction
            case "L":
                if (col - 1) % self.FACE_SIZE != 0:
                    return self._grid[row][col - 1], direction
            case "U":
                if (row - 1) % self.FACE_SIZE != 0:
                    return self._grid[row - 1][col], direction

        # match the face where we're at, where the faces are:
        # +---+
        # | 12|
        # | 3 |
        # |45 |
        # |6  |
        # +---+

        # match face 1
        if row in range(self.FACE_SIZE * 0 + 1, self.FACE_SIZE * 1 + 1) and (
            col in range(self.FACE_SIZE * 1 + 1, self.FACE_SIZE * 2 + 1)
        ):
            match direction:
                case "R":
                    return self._grid[row][col + 1], "R"
                case "D":
                    return self._grid[row + 1][col], "D"
                case "L":
                    return self._grid[(self.FACE_SIZE * 3 + 1) - row][1], "R"
                case "U":
                    return self._grid[(self.FACE_SIZE * 2) + col][1], "R"
        # match face 2
        elif row in range(self.FACE_SIZE * 0 + 1, self.FACE_SIZE * 1 + 1) and (
            col in range(self.FACE_SIZE * 2 + 1, self.FACE_SIZE * 3 + 1)
        ):
            match direction:
                case "R":
                    return self._grid[(self.FACE_SIZE * 3 + 1) - row][(self.FACE_SIZE * 2)], "L"
                case "D":
                    return self._grid[col - self.FACE_SIZE][(self.FACE_SIZE * 2)], "L"
                case "L":
                    return self._grid[row][col - 1], "L"
                case "U":
                    return self._grid[self.FACE_SIZE * 4][col - (self.FACE_SIZE * 2)], "U"
        # match face 3
        elif row in range(self.FACE_SIZE * 1 + 1, self.FACE_SIZE * 2 + 1) and (
            col in range(self.FACE_SIZE * 1 + 1, self.FACE_SIZE * 2 + 1)
        ):
            match direction:
                case "R":
                    return self._grid[self.FACE_SIZE][row + self.FACE_SIZE], "U"
                case "D":
                    return self._grid[row + 1][col], "D"
                case "L":
                    return self._grid[(self.FACE_SIZE * 2 + 1)][row - self.FACE_SIZE], "D"
                case "U":
                    return self._grid[row - 1][col], "U"
        # match face 4
        elif row in range(self.FACE_SIZE * 2 + 1, self.FACE_SIZE * 3 + 1) and (
            col in range(self.FACE_SIZE * 0 + 1, self.FACE_SIZE * 1 + 1)
        ):
            match direction:
                case "R":
                    return self._grid[row][col + 1], "R"
                case "D":
                    return self._grid[row + 1][col], "D"
                case "L":
                    return self._grid[(self.FACE_SIZE * 3 + 1) - row][(self.FACE_SIZE + 1)], "R"
                case "U":
                    return self._grid[col + self.FACE_SIZE][(self.FACE_SIZE + 1)], "R"
        # match face 5
        elif row in range(self.FACE_SIZE * 2 + 1, self.FACE_SIZE * 3 + 1) and (
            col in range(self.FACE_SIZE * 1 + 1, self.FACE_SIZE * 2 + 1)
        ):
            match direction:
                case "R":
                    return self._grid[(self.FACE_SIZE * 3 + 1) - row][(self.FACE_SIZE * 3)], "L"
                case "D":
                    return self._grid[col + (self.FACE_SIZE * 2)][self.FACE_SIZE], "L"
                case "L":
                    return self._grid[row][col - 1], "L"
                case "U":
                    return self._grid[row - 1][col], "U"
        # match face 6
        elif row in range(self.FACE_SIZE * 3 + 1, self.FACE_SIZE * 4 + 1) and (
            col in range(self.FACE_SIZE * 0 + 1, self.FACE_SIZE * 1 + 1)
        ):
            match direction:
                case "R":
                    return self._grid[(self.FACE_SIZE * 3)][row - (self.FACE_SIZE * 2)], "U"
                case "D":
                    return self._grid[1][col + (self.FACE_SIZE * 2)], "D"
                case "L":
                    return self._grid[1][row - (self.FACE_SIZE * 2)], "D"
                case "U":
                    return self._grid[row - 1][col], "U"

        raise ValueError(f"invalid row {row} and col {col}!")

    def get_password(self) -> int:
        password = 1000 * self._current_tile.row
        password += 4 * self._current_tile.col
        match self._direction:
            case "R":
                return password + 0
            case "D":
                return password + 1
            case "L":
                return password + 2
            case "U":
                return password + 3
        raise ValueError(f"invalid direction {self._direction}!")
