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


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.width: int = 71
        self.height: int = 71

    def parse_input(self):
        self.corrupted_space: dict[str, bool] = {}
        for line in self.lines[:1024]:
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
        self.parse_input()
        # add start pos in the bottom left
        start_pos: Pos = Pos(0, self.height - 1)
        # add to flood fill dict and to visited positions
        self.state_dict: dict[int, list[Pos]] = {0: [start_pos]}
        self.visited_pos: dict[str, int] = {str(start_pos): 0}
        while str(Pos(self.width - 1, 0)) not in self.visited_pos:
            self.cycle()
        self.result: int = self.visited_pos[str(Pos(self.width - 1, 0))]

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
