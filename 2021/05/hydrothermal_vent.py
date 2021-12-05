class HydrothermalVent:
    def __init__(self):
        self._horizontal_size = 0
        self._vertical_size = 0
        self._vent_dict = {}

    def add_hv_vent_line(self, x1, y1, x2, y2):
        self._horizontal_size = max([self._horizontal_size, x1 + 1, x2 + 1])
        self._vertical_size = max([self._vertical_size, y1 + 1, y2 + 1])
        # add a horizontal line
        if y1 == y2:
            if self._vent_dict.get(y1) is None:
                self._vent_dict[y1] = {}
            for x in range(min([x1, x2]), max([x1, x2]) + 1):
                self._vent_dict[y1][x] = self._vent_dict[y1].get(x, 0) + 1
        # add a vertical line
        if x1 == x2:
            for y in range(min([y1, y2]), max([y1, y2]) + 1):
                if self._vent_dict.get(y) is None:
                    self._vent_dict[y] = {}
                self._vent_dict[y][x1] = self._vent_dict[y].get(x1, 0) + 1

    def add_hvd_vent_line(self, x1, y1, x2, y2):
        # add horizontal and vertical lines in this function (also update size)
        self.add_hv_vent_line(x1, y1, x2, y2)
        # add diagonal line
        if x1 != x2 and y1 != y2:
            # make sure x1 < x2, otherwise swap the points
            if x1 > x2:
                (x1, y1, x2, y2) = (x2, y2, x1, y1)
            for i in range(x2 - x1 + 1):
                x = x1 + i
                y = y1 + i if y1 < y2 else y1 - i
                if self._vent_dict.get(y) is None:
                    self._vent_dict[y] = {}
                self._vent_dict[y][x] = self._vent_dict[y].get(x, 0) + 1

    def print_field(self):
        for y in range(self._vertical_size):
            for x in range(self._horizontal_size):
                print(self._vent_dict.get(y, {}).get(x, "."), end="")
            print()  # print the newline

    def sum_of_at_least_2(self):
        _sum = 0
        for y in range(self._vertical_size):
            for x in range(self._horizontal_size):
                _sum += self._vent_dict.get(y, {}).get(x, 0) >= 2
        return _sum
