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
        self.width: int = len(self.lines[0])
        self.height: int = len(self.lines)
        self.cheat_distance: int = 20

    def parse_input(self):
        self.track_pos: dict[Pos, bool] = {}
        self.start: Pos | None = None
        self.end: Pos | None = None
        for x in range(self.width):
            for y in range(self.height):
                match self.lines[self.height - y - 1][x]:
                    case ".":
                        # add a track position
                        self.track_pos[Pos(x, y)] = True
                    case "S":
                        # add the start position and track position
                        self.start = Pos(x, y)
                        self.track_pos[Pos(x, y)] = True
                    case "E":
                        # add the end position and track position
                        self.end = Pos(x, y)
                        self.track_pos[Pos(x, y)] = True
                    case _:
                        # wall or something else, ignore
                        pass
        assert self.start and self.end

    def check_race_pos(self, pos: Pos) -> Pos | None:
        # check if the position is on the track, then plan the path
        if pos in self.track_pos and pos not in self.track:
            self.current_pico_second += 1
            self.track[pos] = self.current_pico_second
            return pos
        return None

    def initial_race(self):
        assert self.start and self.end
        pos: Pos = self.start
        self.current_pico_second: int = 0
        self.track: dict[Pos, int] = {pos: self.current_pico_second}
        # continue to move along the track until the end is reached
        while pos != self.end:
            if next_pos := self.check_race_pos(Pos(pos.x + 1, pos.y)):
                pos = next_pos
            elif next_pos := self.check_race_pos(Pos(pos.x - 1, pos.y)):
                pos = next_pos
            elif next_pos := self.check_race_pos(Pos(pos.x, pos.y + 1)):
                pos = next_pos
            elif next_pos := self.check_race_pos(Pos(pos.x, pos.y - 1)):
                pos = next_pos
            else:
                assert False

    def cheat_pos(self, start_pos: Pos):
        self.cheats_store[start_pos] = {}
        # calculate the maximum cheat distance square around the start pos
        xmin = max(0, start_pos.x - self.cheat_distance)
        xmax = min(self.width, start_pos.x + self.cheat_distance)
        ymin = max(0, start_pos.y - self.cheat_distance)
        ymax = min(self.height, start_pos.y + self.cheat_distance)
        # loop through all possible positions
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                end_pos: Pos = Pos(x, y)
                # ensure the end position is on the track
                if end_pos not in self.track:
                    continue
                # calculate the distance and cheat value, add if enough
                distance = abs(start_pos.x - end_pos.x) + abs(start_pos.y - end_pos.y)
                if distance <= self.cheat_distance:
                    cheat_value: int = self.track[end_pos] - self.track[start_pos] - distance
                    if cheat_value >= 100:
                        if cheat_value not in self.cheats:
                            self.cheats[cheat_value] = 0
                        self.cheats[cheat_value] += 1
                        self.cheats_store[start_pos][end_pos] = True

    def cheat(self):
        self.cheats: dict[int, int] = {}
        self.cheats_store: dict[Pos, dict[Pos, bool]] = {}
        for pos in self.track.keys():
            self.cheat_pos(pos)

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.initial_race()
        self.cheat()
        self.result: int = sum(self.cheats.values())

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
