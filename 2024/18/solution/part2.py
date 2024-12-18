from pathlib import Path


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

    def __hash__(self) -> int:
        return hash(str(self))


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.width: int = 71
        self.height: int = 71

    def parse_input(self, until: int):
        self.corrupted_space: dict[str, bool] = {}
        for line in self.lines[:until]:
            x, y = map(int, line.split(","))
            self.corrupted_space[str(Pos(x, self.height - y - 1))] = True

    def move(self, pos: Pos, next_score: int):
        # check that we're out of bounds
        if pos.x < 0 or pos.x >= self.width:
            return
        if pos.y < 0 or pos.y >= self.height:
            return
        # check that the position is corrupted
        if self.corrupted_space.get(str(pos)):
            return
        # check if we have visited before with a lower score
        if str(pos) in self.visited_pos:
            if self.visited_pos[str(pos)] < next_score:
                return
        # move to the position and add to cache
        if next_score not in self.state_dict:
            self.state_dict[next_score] = []
        self.state_dict[next_score].append(pos)
        self.visited_pos[str(pos)] = next_score

    def cycle(self):
        lowest_score: int = min(self.state_dict.keys())
        next_score: int = lowest_score + 1
        # cycle through all unique positions with this score
        for pos in set(self.state_dict[lowest_score]):
            # try to move in all 4 directions
            self.move(Pos(pos.x, pos.y + 1), next_score)
            self.move(Pos(pos.x, pos.y - 1), next_score)
            self.move(Pos(pos.x + 1, pos.y), next_score)
            self.move(Pos(pos.x - 1, pos.y), next_score)
        # remove the current lowest score
        del self.state_dict[lowest_score]

    def solve(self) -> None:
        print("solving...")
        # we know that with 1024 corrupted positions the end is still reachable
        until: int = 1024
        # start increasing the value quickly in the beginning
        course: bool = True
        # simulate a flood fill of the map
        while True:
            self.parse_input(until)
            # add start pos in the bottom left
            start_pos: Pos = Pos(0, self.height - 1)
            # add to flood fill dict and to visited positions
            self.state_dict: dict[int, list[Pos]] = {0: [start_pos]}
            self.visited_pos: dict[str, int] = {str(start_pos): 0}
            # while we have positions to process, process them
            while self.state_dict:
                self.cycle()
            # check if the end is still in the visited positions
            if str(Pos(self.width - 1, 0)) in self.visited_pos:
                # increase the fallen bytes with a course or fine value
                until += 100 if course else 1
            else:
                # otherwise, if in course mode, transition to fine
                if course:
                    course = False
                    until -= 99
                    continue
                # the result is the byte (line) that blocked the end
                self.result: str = self.lines[until - 1]
                break

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
