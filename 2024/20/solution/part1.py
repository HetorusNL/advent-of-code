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
        self.width: int = len(self.lines[0])
        self.height: int = len(self.lines)
        self.cheat_distance: int = 2

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

    def is_inside(self, pos: Pos):
        if pos.x < 0 or pos.x >= self.width:
            return False
        if pos.y < 0 or pos.y >= self.height:
            return False
        return True

    def check_cheat_pos(self, pos: Pos, cheat_path: list[Pos], end_positions: list[Pos]) -> list[Pos] | None:
        # if this position is not in the cheat path yet, add it
        if pos not in cheat_path and self.is_inside(pos):
            new_cheat_path: list[Pos] = cheat_path.copy()
            new_cheat_path.append(pos)
            if len(new_cheat_path) <= self.cheat_distance:
                # we have not cheated the maximum distance, recurse
                self.cheat_pos(pos, new_cheat_path, end_positions)
            else:
                # otherwise add the end position
                end_positions.append(pos)
            return new_cheat_path
        return None

    def cheat_pos(self, pos: Pos, cheat_path: list[Pos], end_positions: list[Pos]) -> list[Pos]:
        # try to move to all 4 positions reachable from pos
        self.check_cheat_pos(Pos(pos.x + 1, pos.y), cheat_path, end_positions)
        self.check_cheat_pos(Pos(pos.x - 1, pos.y), cheat_path, end_positions)
        self.check_cheat_pos(Pos(pos.x, pos.y + 1), cheat_path, end_positions)
        self.check_cheat_pos(Pos(pos.x, pos.y - 1), cheat_path, end_positions)
        return end_positions

    def process_cheat_positions(self, start_pos: Pos, end_positions: list[Pos]):
        for end_position in end_positions:
            # skip duplicate cheats
            if end_position in self.cheats_store[start_pos]:
                continue
            # calculate the cheat score and add to the cheats dict
            if end_value := self.track.get(end_position):
                cheat_value: int = end_value - self.track[start_pos] - self.cheat_distance
                if cheat_value >= 100:
                    if cheat_value not in self.cheats:
                        self.cheats[cheat_value] = 0
                    self.cheats[cheat_value] += 1
                    self.cheats_store[start_pos][end_position] = True

    def cheat(self):
        self.cheats: dict[int, int] = {}
        self.cheats_store: dict[Pos, dict[Pos, bool]] = {}
        # move through all start positions, and start the cheat
        for pos in self.track.keys():
            self.cheats_store[pos] = {}
            end_positions: list[Pos] = self.cheat_pos(pos, [pos], [])
            self.process_cheat_positions(pos, end_positions)

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.initial_race()
        self.cheat()
        self.result: int = sum(self.cheats.values())

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
