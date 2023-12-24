from pathlib import Path

from solution.hailstone import Hailstone
from solution.pos2d import Pos2D
from solution.formula2d import Formula2D


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.min_value = 200000000000000
        self.max_value = 400000000000000
        self.value_range = 1000

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        self.hailstones: list[Hailstone] = []
        for line in self.lines:
            self.hailstones.append(Hailstone(line))

        # get the list of equal velocity hailstones
        vx_equal_hailstones: list[tuple[Hailstone, Hailstone]] = []
        vy_equal_hailstones: list[tuple[Hailstone, Hailstone]] = []
        vz_equal_hailstones: list[tuple[Hailstone, Hailstone]] = []
        for first_idx in range(len(self.hailstones)):
            for idx in range(first_idx + 1, len(self.hailstones)):
                hailstone1 = self.hailstones[first_idx]
                hailstone2 = self.hailstones[idx]
                if hailstone1.vx == hailstone2.vx:
                    vx_equal_hailstones.append((hailstone1, hailstone2))
                if hailstone1.vy == hailstone2.vy:
                    vy_equal_hailstones.append((hailstone1, hailstone2))
                if hailstone1.vz == hailstone2.vz:
                    vz_equal_hailstones.append((hailstone1, hailstone2))

        # find common divisors of the equal hailstones, thus its velocity
        # common divisor in x
        vx_divisors: dict[int, int] = {}
        for h1, h2 in vx_equal_hailstones:
            self.add_divisors(abs(h1.x - h2.x), h1.vx, vx_divisors)
        assert any(value == len(vx_equal_hailstones) for value in vx_divisors.values())
        rock_vx = list(filter(lambda key: vx_divisors[key] == len(vx_equal_hailstones), vx_divisors))[0]
        # common divisor in y
        vy_divisors: dict[int, int] = {}
        for h1, h2 in vy_equal_hailstones:
            self.add_divisors(abs(h1.y - h2.y), h1.vy, vy_divisors)
        assert any(value == len(vy_equal_hailstones) for value in vy_divisors.values())
        rock_vy = list(filter(lambda key: vy_divisors[key] == len(vy_equal_hailstones), vy_divisors))[0]
        # common divisor in z
        vz_divisors: dict[int, int] = {}
        for h1, h2 in vz_equal_hailstones:
            self.add_divisors(abs(h1.z - h2.z), h1.vz, vz_divisors)
        assert any(value == len(vz_equal_hailstones) for value in vz_divisors.values())
        rock_vz = list(filter(lambda key: vz_divisors[key] == len(vz_equal_hailstones), vz_divisors))[0]

        # solve for start position using math magic
        hailstone1 = self.hailstones[0]
        hailstone2 = self.hailstones[1]
        t2_numerator = (
            hailstone2.y
            - hailstone1.y
            - (((hailstone1.vy - rock_vy) * (hailstone2.x - hailstone1.x)) / (hailstone1.vx - rock_vx))
        )
        t2_denumerator = (
            rock_vy
            - hailstone2.vy
            - (((hailstone1.vy - rock_vy) * (rock_vx - hailstone2.vx)) / (hailstone1.vx - rock_vx))
        )
        t2 = t2_numerator / t2_denumerator
        t1 = (hailstone2.x - hailstone1.x - t2 * (rock_vx - hailstone2.vx)) / (hailstone1.vx - rock_vx)
        rock_startx = hailstone1.x - t1 * (rock_vx - hailstone1.vx)
        rock_starty = hailstone1.y - t1 * (rock_vy - hailstone1.vy)
        rock_startz = hailstone1.z - t1 * (rock_vz - hailstone1.vz)
        self.result = int(rock_startx + rock_starty + rock_startz)

    def add_divisors(self, pos_diff: int, speed: int, divisors: dict[int, int]) -> None:
        for i in range(-self.value_range, self.value_range):
            if i == 0:
                continue
            if pos_diff % i == 0:
                divisor = i + speed
                if divisor not in divisors:
                    divisors[divisor] = 0
                divisors[divisor] += 1

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
