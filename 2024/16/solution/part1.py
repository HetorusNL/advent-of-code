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

    def __eq__(self, other: object) -> bool:
        assert type(other) == Pos
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"


class State(Pos):
    def __init__(self, pos: Pos, direction: Direction):
        super().__init__(pos.x, pos.y)
        self.pos: Pos = pos
        self.direction: Direction = direction

    def __eq__(self, other: object) -> bool:
        assert type(other) == State
        return self.pos == other.pos and self.direction == other.direction

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}, {self.direction}]"


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.width: int = len(self.lines[0])
        self.height: int = len(self.lines)

    def parse_input(self):
        self.path: dict[str, bool] = {}
        self.start: Pos | None = None
        self.end: Pos | None = None

        # make the grid with the origin in the bottom left
        for x in range(self.width):
            for y in range(self.height):
                match self.lines[self.height - y - 1][x]:
                    case "S":
                        # we can only have 1 start
                        assert self.start is None
                        self.start = Pos(x, y)
                    case "E":
                        # we can only have 1 end
                        assert self.end is None
                        self.end = Pos(x, y)
                    case "#":
                        # we don't care about walls, continue to the next
                        continue
                    case _:
                        # nothing to do here, as it's a path
                        pass
                # in this case we have a start, end or a pos on the path
                self.path[str(Pos(x, y))] = True

    def move(self, pos: Pos, direction: Direction, new_score: int):
        # if not a path, can't move
        if str(pos) not in self.path:
            return
        # construct a new state
        state: State = State(pos, direction)
        # if in visited states cache, don't move
        if str(state) in self.visited_states:
            return
        # otherwise add the move to the new score
        if new_score not in self.state_dict:
            self.state_dict[new_score] = []
        self.state_dict[new_score].append(state)
        # and add to visited states cache
        self.visited_states[str(state)] = True

    def process_state(self, state: State, score: int):
        pos: Pos = state.pos
        # depending on the direction, move to all possible positions
        match state.direction:
            case Direction.UP:
                # move up
                self.move(Pos(pos.x, pos.y + 1), Direction.UP, score + 1)
                # move left
                self.move(Pos(pos.x - 1, pos.y), Direction.LEFT, score + 1001)
                # move right
                self.move(Pos(pos.x + 1, pos.y), Direction.RIGHT, score + 1001)
            case Direction.RIGHT:
                # move right
                self.move(Pos(pos.x + 1, pos.y), Direction.RIGHT, score + 1)
                # move up
                self.move(Pos(pos.x, pos.y + 1), Direction.UP, score + 1001)
                # move down
                self.move(Pos(pos.x, pos.y - 1), Direction.DOWN, score + 1001)
            case Direction.DOWN:
                # move down
                self.move(Pos(pos.x, pos.y - 1), Direction.DOWN, score + 1)
                # move left
                self.move(Pos(pos.x - 1, pos.y), Direction.LEFT, score + 1001)
                # move right
                self.move(Pos(pos.x + 1, pos.y), Direction.RIGHT, score + 1001)
            case Direction.LEFT:
                # move left
                self.move(Pos(pos.x - 1, pos.y), Direction.LEFT, score + 1)
                # move up
                self.move(Pos(pos.x, pos.y + 1), Direction.UP, score + 1001)
                # move down
                self.move(Pos(pos.x, pos.y - 1), Direction.DOWN, score + 1001)

    def cycle(self) -> bool:
        lowest_score: int = min(self.state_dict.keys())
        # check if any of the states with this score are at the end pos
        if any(state.pos == self.end for state in self.state_dict[lowest_score]):
            return True
        # process all states
        for state in self.state_dict[lowest_score]:
            self.process_state(state, lowest_score)
        # remove the state from the list
        del self.state_dict[lowest_score]
        # no end yet
        return False

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        assert self.start and self.end
        # add the initial position, and backward position (should be wall anyways)
        start_forward: State = State(self.start, Direction.RIGHT)
        start_backward: State = State(self.start, Direction.LEFT)
        # connection between score and the list of states that have that score
        self.state_dict: dict[int, list[State]] = {0: [start_forward], 2000: [start_backward]}
        # a cache for the visisted states, so we don't visit them again
        self.visited_states: dict[str, bool] = {str(start_forward): True, str(start_backward): True}
        # continuously cycle until we get to the end position with lowest score
        while True:
            if self.cycle():
                break
        # score is the lowest
        self.result: int = min(self.state_dict.keys())

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
