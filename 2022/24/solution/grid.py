from solution.blizzard import Blizzard
from solution.gridpos import GridPos


class Grid:
    def __init__(self, lines: list[str]):
        self._blizzards: dict[str, list[Blizzard]] = {}
        self._edge: dict[str, bool] = {}
        self._width = len(lines[0]) - 2
        self._height = len(lines) - 2
        self._positions: list[GridPos] = [GridPos(0, -1)]
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                # the coordinate system is transformed so that the blizzard grid starts at [0, 0]
                # check for wall, if so add to edge array
                if char == "#":
                    self._edge[f"[{x-1}, {y-1}]"] = True
                elif char in "><^v":
                    blizzard = Blizzard(x - 1, y - 1, char, self._width, self._height)
                    self._blizzards[blizzard.pos] = [blizzard]
                else:
                    assert char == "."

        self._cache_hits = 0

        self._goals: list[GridPos] = []
        self._goal: GridPos = GridPos(self._width - 1, self._height)

    def go_back_and_forth(self) -> None:
        # add the goals to go back and forth to the list
        self._goals.append(GridPos(0, -1))
        self._goals.append(GridPos(self._width - 1, self._height))

    def update(self) -> None:
        self._update_blizzards()

        new_pos: list[GridPos] = []
        cache: dict[str, bool] = {}
        for position in self._positions:
            pos_surround = [
                pos
                for pos in self._pos_surround(position)
                if pos.pos not in self._edge and pos.pos not in self._blizzards
            ]
            for pos in pos_surround:
                if cache.get(pos.pos):
                    self._cache_hits += 1
                else:
                    cache[pos.pos] = True
                    new_pos.append(pos)
        self._positions = new_pos

        # update goals
        if self.goal_reached():
            if len(self._goals):
                # extract the new goal
                new_goal = self._goals.pop(0)
                # update the positions to start at the goal position
                self._positions = [self._goal]
                # overwrite the goal with the new goal
                self._goal = new_goal

    def _update_blizzards(self) -> None:
        new_blizzards: dict[str, list[Blizzard]] = {}
        for blizzards in self._blizzards.values():
            for blizzard in blizzards:
                blizzard.update()
                if blizzard.pos not in new_blizzards:
                    new_blizzards[blizzard.pos] = []
                new_blizzards[blizzard.pos].append(blizzard)
        self._blizzards = new_blizzards

    def _pos_surround(self, pos: GridPos) -> list[GridPos]:
        # return all positions around the player (including current pos)
        positions: list[GridPos] = [GridPos(pos.x, pos.y)]  # current position
        if pos.y >= 0:
            positions.append(GridPos(pos.x, pos.y - 1))
        if pos.y < self._height:
            positions.append(GridPos(pos.x, pos.y + 1))
        if pos.x >= 0:
            positions.append(GridPos(pos.x - 1, pos.y))
        if pos.x < self._width:
            positions.append(GridPos(pos.x + 1, pos.y))
        return positions

    def goal_reached(self):
        return any(pos == self._goal for pos in self._positions)
