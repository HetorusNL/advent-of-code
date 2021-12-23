from typing import List, Tuple


class Burrow1:
    # constants
    _w = 11
    _h = 3
    _energy_lut = {"A": 1, "B": 10, "C": 100, "D": 1000}
    _amphipods = _energy_lut  # to use <..> in self._amphipods
    _room_x = {"A": 2, "B": 4, "C": 6, "D": 8}

    def __init__(self, amphipods: Tuple[List[List[str]], None] = None):
        # variables
        self._grid: List[List[str]] = []  # grid [y] [x]
        [self._grid.append([""] * self._w) for _ in range(self._h)]
        if amphipods:
            for y in range(2):
                for x in range(4):
                    self._grid[y + 1][x * 2 + 2] = amphipods[y][x]
        self._energy = 0
        self._finished = False

    def copy(self):
        # create new empty instance
        new = Burrow1()
        # copy over the variables
        for y in range(self._h):
            new._grid[y] = self._grid[y].copy()
        new._energy = self._energy
        return new

    def print(self):
        for y in range(self._h):
            print("".join(a if a else "." for a in self._grid[y]))

    def simulate(self):
        new_burrows = []
        # check the hallway amphipods
        for x in range(self._w):
            if self._grid[0][x] in self._amphipods:
                new_burrows.extend(self._handle_hallway_amphipod(x))
        # check the room amphipods
        for y in [2, 1]:
            for x in range(self._w):
                if self._grid[y][x] in self._amphipods:
                    new_burrows.extend(self._handle_room_amphipod(y, x))
        return new_burrows

    def _handle_hallway_amphipod(self, x):
        current_amphipod = self._grid[0][x]
        amphipod_room_x = self._room_x[current_amphipod]

        # handle the case that there's a wrong amphipod at y = 2 or y = 1
        for y in [2, 1]:
            current_room_inhabitant = self._grid[y][amphipod_room_x]
            if current_room_inhabitant:
                if current_room_inhabitant != current_amphipod:
                    return []  # invalid amphipod at destination y and x

        # verify that the hallway till the room is clear
        if x < amphipod_room_x:
            for path_x in range(x + 1, amphipod_room_x + 1):
                if self._grid[0][path_x]:
                    return []  # amphipod in the way in the hallway
        if x > amphipod_room_x:
            for path_x in range(amphipod_room_x, x):
                if self._grid[0][path_x]:
                    return []  # amphipod in the way in the hallway

        # place the amphipod in the lowest free space in the room
        for y in [2, 1]:
            if not self._grid[y][amphipod_room_x]:
                return self._create_amphipod(0, x, y, amphipod_room_x)

        assert False  # this can't happen, than the room is already full

    def _handle_room_amphipod(self, y, x):
        # handle the case that there's a amphipod above
        if y == 2 and self._grid[1][x] in self._amphipods:
            return []

        # handle the case that amphipods are already in the currect room
        if y == 2 and self._room_x.get(self._grid[y][x]) == x:
            return []
        if y == 1 and self._room_x.get(self._grid[2][x]) == x:
            if self._room_x.get(self._grid[y][x]) == x:
                return []

        new_burrows = []
        # check every hallway position where the room amphipod can move to
        for new_x in range(x, -1, -1):  # from current pos to the left
            if new_x in self._room_x.values():
                continue
            if self._grid[y][x] == "D":
                target = self._room_x["D"]
                if new_x not in range(min(x, target), max(x, target) + 1):
                    continue
            if self._grid[0][new_x] in self._amphipods:
                break
            # this is a new position, add it to the new_burrows
            new_burrows.extend(self._create_amphipod(y, x, 0, new_x))
        for new_x in range(x, self._w):  # from current pos to the right
            if new_x in self._room_x.values():
                continue
            if self._grid[y][x] == "D":
                target = self._room_x["D"]
                if new_x not in range(min(x, target), max(x, target) + 1):
                    continue
            if self._grid[0][new_x] in self._amphipods:
                break
            # this is a new position, add it to the new_burrows
            new_burrows.extend(self._create_amphipod(y, x, 0, new_x))
        return new_burrows

    def _create_amphipod(self, old_y, old_x, new_y, new_x):
        energy_per_step = self._energy_lut[self._grid[old_y][old_x]]
        steps = abs(new_y - old_y) + abs(new_x - old_x)
        new_burrow = self.copy()
        new_burrow._grid[new_y][new_x] = new_burrow._grid[old_y][old_x]
        new_burrow._grid[old_y][old_x] = ""
        new_burrow._energy += energy_per_step * steps
        if new_burrow._energy > 13500:
            return []
        for y in [1, 2]:
            for amphipod in self._amphipods:
                if new_burrow._grid[y][self._room_x[amphipod]] != amphipod:
                    return [new_burrow]
        new_burrow._finished = True
        return [new_burrow]
