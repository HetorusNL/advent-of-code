import re
from typing import Union

from solution.tile import Tile


class Grid2D:
    def __init__(self, lines: list[str]):
        map_regex = re.compile(r"^[.# ]*$")
        path_regex = re.compile(r"^[0-9RL]*$")
        number_regex = re.compile(r"^(?P<number>[0-9]*)")
        direction_regex = re.compile(r"^(?P<direction>[LR])")
        self._grid: dict[int, dict[int, Tile]] = {}
        self._instructions: list[Union[int, str]] = []

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
                match self._direction:
                    case "R":
                        for _ in range(instruction):
                            if not self._move_performed(self._current_tile.row, self._current_tile.col + 1):
                                break
                    case "D":
                        for _ in range(instruction):
                            if not self._move_performed(self._current_tile.row + 1, self._current_tile.col):
                                break
                    case "L":
                        for _ in range(instruction):
                            if not self._move_performed(self._current_tile.row, self._current_tile.col - 1):
                                break
                    case "U":
                        for _ in range(instruction):
                            if not self._move_performed(self._current_tile.row - 1, self._current_tile.col):
                                break
            elif type(instruction) is str:
                match instruction:
                    case "R":
                        # rotate to the right (clockwise)
                        self._direction = {"R": "D", "D": "L", "L": "U", "U": "R"}[self._direction]
                    case "L":
                        # rotate to the right (clockwise)
                        self._direction = {"R": "U", "U": "L", "L": "D", "D": "R"}[self._direction]

    def _move_performed(self, row: int, col: int) -> bool:
        if tile := self._grid.get(row, {}).get(col):
            if tile.is_open:
                self._current_tile.row = tile.row
                self._current_tile.col = tile.col
                return True
            elif tile.is_wall:
                return False
        # no tile found, wrap around
        wrap_tile = self._get_wrap_tile(row, col, self._direction)
        if wrap_tile.is_open:
            self._current_tile.row = wrap_tile.row
            self._current_tile.col = wrap_tile.col
            return True
        return False

    def _get_wrap_tile(self, row: int, col: int, direction: str) -> Tile:
        match direction:
            case "R":
                # return leftmost tile on the same row
                new_col = min(tile.col for tile in self._grid[row].values() if tile.is_present)
                return self._grid[row][new_col]
            case "D":
                # return upmost tile (lowest number) in the same col
                new_row = min(row[col].row for row in self._grid.values() if row.get(col) and row[col].is_present)
                return self._grid[new_row][col]
            case "L":
                # return rightmost tile on the same row
                new_col = max(tile.col for tile in self._grid[row].values() if tile.is_present)
                return self._grid[row][new_col]
            case "U":
                # return downmost tile (highest number) in the same col
                new_row = max(row[col].row for row in self._grid.values() if row.get(col) and row[col].is_present)
                return self._grid[new_row][col]
        raise ValueError(f"invalid direction {direction}!")

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
