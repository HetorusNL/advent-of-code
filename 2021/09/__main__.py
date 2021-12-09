class Solution:
    def __init__(self):
        # the height map
        self._hm = []
        self._low_points = []

        with open("input.txt") as f:
            lines = f.readlines()

        for line in lines:
            self._hm.append([int(h) for h in line.strip()])

    def solve(self):
        self.part_1()
        self.part_2()

    def part_1(self):
        width = len(self._hm[0])
        height = len(self._hm)
        low_point_risk_level = 0
        for y in range(height):
            for x in range(width):
                # calculate x (not) low points
                if x > 0 and self._hm[y][x - 1] <= self._hm[y][x]:
                    continue
                if x < (width - 1) and self._hm[y][x + 1] <= self._hm[y][x]:
                    continue
                # calculate y (not) low points
                if y > 0 and self._hm[y - 1][x] <= self._hm[y][x]:
                    continue
                if y < (height - 1) and self._hm[y + 1][x] <= self._hm[y][x]:
                    continue
                # found a low point
                self._low_points.append({"x": x, "y": y})
                low_point_risk_level += 1 + self._hm[y][x]
        print(f"heightmap low points risk level sum: {low_point_risk_level}")

    def part_2(self):
        basin_sizes = []
        for low_point in self._low_points:
            points = [{"x": low_point["x"], "y": low_point["y"]}]
            index = 0
            while index < len(points):
                found_points = self._check_point(points[index])
                for p in found_points:
                    points.append(p)
                index += 1
            basin_sizes.append(len(set(tuple(p.items()) for p in points)))
        basin_sizes.sort()
        largest_3_basins = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]
        print(f"largest 3 basin size multiplied together: {largest_3_basins}")

    def _check_point(self, point):
        new_points = []
        width = len(self._hm[0])
        height = len(self._hm)
        x = point["x"]
        y = point["y"]
        point_height = self._hm[y][x]
        # calculate x heigher points
        if x > 0 and self._hm[y][x - 1] >= point_height + 1:
            new_points.append({"x": x - 1, "y": y})
        if x < (width - 1) and self._hm[y][x + 1] >= point_height + 1:
            new_points.append({"x": x + 1, "y": y})
        # calculate y heigher points
        if y > 0 and self._hm[y - 1][x] >= point_height + 1:
            new_points.append({"x": x, "y": y - 1})
        if y < (height - 1) and self._hm[y + 1][x] >= point_height + 1:
            new_points.append({"x": x, "y": y + 1})
        # make sure that the height isn't 9
        new_points = [p for p in new_points if self._hm[p["y"]][p["x"]] != 9]
        return new_points


if __name__ == "__main__":
    Solution().solve()
