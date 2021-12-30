from typing import Dict


class SeaCucumbers:
    def __init__(self):
        self.w = None
        self.h = 0
        self._east_map: Dict[int, Dict[int, bool]] = {}
        self._south_map: Dict[int, Dict[int, bool]] = {}

    def add_line(self, line):
        # update the width and height
        if self.w is None:
            self.w = len(line)
        assert self.w == len(line)
        self.h += 1
        # add a line to the map
        self._east_map[self.h - 1] = {}
        self._south_map[self.h - 1] = {}
        for x in range(len(line)):
            if line[x] == ">":
                self._east_map[self.h - 1][x] = True
            elif line[x] == "v":
                self._south_map[self.h - 1][x] = True
        return self

    def step(self):
        east_result = self._step_east()
        south_result = self._step_south()
        return east_result or south_result

    def _step_east(self):
        new_east_map = {}
        added_to_map = False
        # process all current positions
        for y in self._east_map:
            for x in self._east_map[y]:
                new_x = (x + 1) % self.w
                # check if an east sea cucumber exists on the next pos
                if self._east_map[y].get(new_x):
                    self._add_to_map(new_east_map, y, x)
                    continue
                # check if a south sea cucumber exists on the next pos
                if self._south_map.get(y, {}).get(new_x):
                    self._add_to_map(new_east_map, y, x)
                    continue
                self._add_to_map(new_east_map, y, new_x)
                added_to_map = True
        self._east_map = new_east_map
        return added_to_map

    def _step_south(self):
        new_south_map = {}
        added_to_map = False
        # process all current positions
        for y in self._south_map:
            new_y = (y + 1) % self.h
            for x in self._south_map[y]:
                # check if a east sea cucumber exists on the next pos
                if self._east_map.get(new_y, {}).get(x):
                    self._add_to_map(new_south_map, y, x)
                    continue
                # check if a south sea cucumber exists on the next pos
                if self._south_map.get(new_y, {}).get(x):
                    self._add_to_map(new_south_map, y, x)
                    continue
                self._add_to_map(new_south_map, new_y, x)
                added_to_map = True
        self._south_map = new_south_map
        return added_to_map

    def _add_to_map(self, _map, y, x):
        if y not in _map:
            _map[y] = {}
        _map[y][x] = True

    def print(self):
        print("see cucumbers map:")
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                if self._east_map.get(y, {}).get(x):
                    row += ">"
                elif self._south_map.get(y, {}).get(x):
                    row += "v"
                else:
                    row += "."
            print(row)
