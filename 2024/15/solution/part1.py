from enum import auto
from enum import Enum
from pathlib import Path


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class Pos:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def parse_input(self):
        self.height: int = -1
        self.width: int = len(self.lines[0])
        is_map = True
        _map: dict[int, dict[int, str]] = {}
        self.moves: list[Direction] = []
        self.robot = None
        # loop through all lines, and let y increase for every line
        for y, line in enumerate(self.lines):
            # check that we have either a map line or direction line
            if line:
                # check if we had an empty line separating map from direction
                if is_map:
                    # add the character to the map dict
                    for x, char in enumerate(line):
                        # add every new y to the map
                        if y not in _map:
                            _map[y] = {}
                        if char == "@":
                            # add the robot, making sure to only add 1
                            assert self.robot is None
                            self.robot = Pos(x, y)
                            # robot position is also a "."
                            _map[y][x] = "."
                        else:
                            # otherwise add the character to the map
                            _map[y][x] = char
                else:
                    # for every direction line, add direction enum to the list
                    for direction in line:
                        match direction:
                            case "^":
                                self.moves.append(Direction.UP)
                            case "v":
                                self.moves.append(Direction.DOWN)
                            case "<":
                                self.moves.append(Direction.LEFT)
                            case ">":
                                self.moves.append(Direction.RIGHT)
                            case _:
                                assert False
            else:
                # found empty line, transition from map to direction
                self.height: int = y
                is_map = False
        # checks that we found the information needed
        assert self.height != -1
        assert self.robot
        # store the map and robot in coordinates with the origin in the bottom left
        self.map: list[list[str]] = []
        for x in range(self.width):
            self.map.append([])
            for y in range(self.height):
                self.map[x].append(_map[self.height - y - 1][x])
        self.robot = Pos(self.robot.x, self.height - self.robot.y - 1)

    def move_direction(self, x_move: int, y_move: int):
        initial_x_move: int = x_move
        initial_y_move: int = y_move
        # to please the type checker
        assert self.robot
        while True:
            match self.map[self.robot.x + x_move][self.robot.y + y_move]:
                case "O":
                    # one additional box to move
                    x_move += initial_x_move
                    y_move += initial_y_move
                case ".":
                    # found empty space, perform the move
                    self.map[self.robot.x + x_move][self.robot.y + y_move] = "O"
                    self.map[self.robot.x + initial_x_move][self.robot.y + initial_y_move] = "."
                    self.robot = Pos(self.robot.x + initial_x_move, self.robot.y + initial_y_move)
                    return
                case "#":
                    # found a wall, bail out
                    return
                case _:
                    assert False

    def move_robot(self):
        for move in self.moves:
            match move:
                case Direction.UP:
                    self.move_direction(0, 1)
                case Direction.DOWN:
                    self.move_direction(0, -1)
                case Direction.LEFT:
                    self.move_direction(-1, 0)
                case Direction.RIGHT:
                    self.move_direction(1, 0)

    def calculate_gps(self):
        self.result = 0
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                # add a calculated value for every box found
                if self.map[x][y] == "O":
                    self.result += (self.height - y - 1) * 100 + x * 1

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.move_robot()
        self.calculate_gps()

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
