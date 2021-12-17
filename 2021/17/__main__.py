import re


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            data = f.readline().strip()

        regexp = r"x=(?P<xmin>[\-0-9]*)\.\.(?P<xmax>[\-0-9]*).*"
        regexp += r"y=(?P<ymin>[\-0-9]*)\.\.(?P<ymax>[\-0-9]*)"
        match = re.search(regexp, data).groupdict()
        self.xmin = int(match["xmin"])
        self.xmax = int(match["xmax"])
        self.ymin = int(match["ymin"])
        self.ymax = int(match["ymax"])

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        hi_y, _ = self._run_simulation()
        print(f"highest y position reached with any initial velocity: {hi_y}")

    def part_2(self):
        _, num_iv = self._run_simulation()
        print(f"number of initial velocities that reach the target: {num_iv}")

    def _run_simulation(self):
        total_highest_y = 0
        num_initial_velocities = 0
        for x_velocity in range(1, self.xmax + 1):
            for y_velocity in range(self.ymin, 500):
                result, highest_y = self._simulate(x_velocity, y_velocity)
                if result:
                    total_highest_y = max(total_highest_y, highest_y)
                    num_initial_velocities += 1
        return total_highest_y, num_initial_velocities

    def _simulate(self, x_velocity, y_velocity):
        x = 0
        y = 0
        highest_y = y
        while True:
            # move in x direction
            x += x_velocity
            # move in y direction
            y += y_velocity
            highest_y = max(highest_y, y)
            # apply drag in x direction
            if x_velocity > 0:
                x_velocity -= 1
            elif x_velocity < 0:
                x_velocity += 1
            # apply drag in y direction
            y_velocity -= 1

            # check if within box
            if self._within_box(x, y):
                return True, highest_y
            # check if below target
            if y < self.ymin:
                return False, highest_y
            # check if past target
            if x > self.xmax:
                return False, highest_y
            # check if before target and x_velocity is zero
            if x < self.xmin and x_velocity == 0:
                return False, highest_y

    def _within_box(self, x, y):
        if x < self.xmin or x > self.xmax:
            return False
        if y < self.ymin or y > self.ymax:
            return False
        return True


if __name__ == "__main__":
    Solution().solve()
