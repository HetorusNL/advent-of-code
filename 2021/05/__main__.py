import copy
from hydrothermal_vent import HydrothermalVent


class Solution:
    def __init__(self):
        with open("input.txt") as f:
            _input = [a.strip() for a in f.readlines()]

        # horizontal and vertical vent
        self.hv_vent = HydrothermalVent()
        # horizontal, vertical and diagonal vent
        self.hvd_vent = HydrothermalVent()

        for line in _input:
            from_to = line.split(" -> ")
            x1, y1 = from_to[0].split(",")
            x2, y2 = from_to[1].split(",")
            self.hv_vent.add_hv_vent_line(int(x1), int(y1), int(x2), int(y2))
            self.hvd_vent.add_hvd_vent_line(int(x1), int(y1), int(x2), int(y2))

    def solve(self):
        self.part_1()
        self.part_2()

    def part_1(self):
        _sum = self.hv_vent.sum_of_at_least_2()
        print(f"number of points where at least 2 (hv) lines overlap {_sum}")

    def part_2(self):
        _sum = self.hvd_vent.sum_of_at_least_2()
        print(f"number of points where at least 2 (hvd) lines overlap {_sum}")


if __name__ == "__main__":
    Solution().solve()
