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


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def parse_input(self):
        self.height: int = -1
        self.width: int = len(self.lines[0] * 2)
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
                            # add the robot, always on the left side, making sure to only add 1
                            assert self.robot is None
                            self.robot = Pos(x * 2, y)
                            _map[y][x * 2] = "."
                            _map[y][x * 2 + 1] = "."
                        elif char == "#" or char == ".":
                            # if we have a wall or empty space, add 2 of them
                            _map[y][x * 2] = char
                            _map[y][x * 2 + 1] = char
                        elif char == "O":
                            # if we have a box, add left and right side of the box
                            _map[y][x * 2] = "["
                            _map[y][x * 2 + 1] = "]"
                        else:
                            assert False
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
        # store the map in coordinates with the origin in the bottom left
        self.map: list[list[str]] = []
        for x in range(self.width):
            self.map.append([])
            for y in range(self.height):
                self.map[x].append(_map[self.height - y - 1][x])
        self.robot = Pos(self.robot.x, self.height - self.robot.y - 1)

    def move_direction(self, direction: Direction):
        # to please the type checker
        assert self.robot
        # shorthand for self.robot
        pos = self.robot
        # different handling for vertical/horizontal moves
        match direction:
            case Direction.LEFT:
                for i in range(1, self.width):
                    new_pos = self.map[pos.x - i][pos.y]
                    match new_pos:
                        case ".":
                            # we can move
                            for last_pos in range(i, 0, -1):
                                self.map[pos.x - last_pos][pos.y] = self.map[pos.x - last_pos + 1][pos.y]
                            self.map[pos.x - 1][pos.y] = "."
                            self.robot = Pos(pos.x - 1, pos.y)
                            return
                        case "#":
                            # found a wall, bail out
                            return
                        case "[" | "]":
                            # valid box, test the next one
                            continue
                        case _:
                            assert False
            case Direction.RIGHT:
                for i in range(1, self.width):
                    new_pos = self.map[pos.x + i][pos.y]
                    match new_pos:
                        case ".":
                            # we can move
                            for last_pos in range(i, 0, -1):
                                self.map[pos.x + last_pos][pos.y] = self.map[pos.x + last_pos - 1][pos.y]
                            self.map[pos.x + 1][pos.y] = "."
                            self.robot = Pos(pos.x + 1, pos.y)
                            return
                        case "#":
                            # found a wall, bail out
                            return
                        case "[" | "]":
                            # valid box, test the next one
                            continue
                        case _:
                            assert False
            case Direction.UP:
                # list of rows with x positions that move up
                x_pos: list[list[int]] = [[self.robot.x]]
                for i in range(self.height):
                    # new list of x positions
                    new_x_pos: list[int] = []
                    # loop through all x positions to move up
                    for x in x_pos[i]:
                        new_pos = self.map[x][pos.y + i + 1]
                        match new_pos:
                            case ".":
                                # we can move
                                pass
                            case "#":
                                # found a wall, bail out
                                return
                            case "[":
                                # found a section of a box, add the box
                                new_x_pos.append(x)
                                new_x_pos.append(x + 1)
                            case "]":
                                # found a section of a box, add the box
                                new_x_pos.append(x - 1)
                                new_x_pos.append(x)
                            case _:
                                assert False
                    if new_x_pos:
                        # add the next row of boxes
                        x_pos.append(new_x_pos)
                    else:
                        # all empty spaces, we can move all boxes
                        if len(x_pos) > 1:
                            # move all unique box locations up
                            for row in range(len(x_pos) - 1, 0, -1):
                                for x in set(x_pos[row]):
                                    # update the row
                                    self.map[x][pos.y + row + 1] = self.map[x][pos.y + row]
                                    # clear the moved position
                                    self.map[x][pos.y + row] = "."
                        # also update the robot up
                        self.robot = Pos(pos.x, pos.y + 1)
                        return
            case Direction.DOWN:
                # list of rows with x positions that move down
                x_pos: list[list[int]] = [[self.robot.x]]
                for i in range(self.height):
                    # new list of x positions
                    new_x_pos: list[int] = []
                    # loop through all x positions to move down
                    for x in x_pos[i]:
                        new_pos = self.map[x][pos.y - i - 1]
                        match new_pos:
                            case ".":
                                # we can move
                                pass
                            case "#":
                                # found a wall, bail out
                                return
                            case "[":
                                # found a section of a box, add the box
                                new_x_pos.append(x)
                                new_x_pos.append(x + 1)
                            case "]":
                                # found a section of a box, add the box
                                new_x_pos.append(x - 1)
                                new_x_pos.append(x)
                            case _:
                                assert False
                    if new_x_pos:
                        # add the next row of boxes
                        x_pos.append(new_x_pos)
                    else:
                        # all empty spaces, we can move all boxes
                        if len(x_pos) > 1:
                            # move all unique box locations down
                            for row in range(len(x_pos) - 1, 0, -1):
                                for x in set(x_pos[row]):
                                    # update the row
                                    self.map[x][pos.y - row - 1] = self.map[x][pos.y - row]
                                    # clear the moved position
                                    self.map[x][pos.y - row] = "."
                        # also update the robot down
                        self.robot = Pos(pos.x, pos.y - 1)
                        return

    def move_robot(self):
        for move in self.moves:
            self.move_direction(move)

    def calculate_gps(self):
        self.result = 0
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                # add a calculated value for every left-side of the box found
                if self.map[x][y] == "[":
                    self.result += (self.height - y - 1) * 100 + x * 1

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.move_robot()
        self.calculate_gps()

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
