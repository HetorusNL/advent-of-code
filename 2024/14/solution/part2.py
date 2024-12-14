from pathlib import Path
import re


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


class Robot:
    def __init__(self, x: int, y: int, vx: int, vy: int):
        self.x: int = x
        self.y: int = y
        self.vx: int = vx
        self.vy: int = vy

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<[{self.x}, {self.y}], [{self.vx}, {self.vy}]>"


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.height: int = 103
        self.width: int = 101
        self.steps: int = 100

    def get_robots(self) -> list[Robot]:
        robots: list[Robot] = []
        for line in self.lines:
            match = re.match(r"^p=(?P<x>[0-9]+),(?P<y>[0-9]+) v=(?P<vx>[0-9-]+),(?P<vy>[0-9-]+)", line)
            assert match
            gd = match.groupdict()
            robots.append(Robot(int(gd["x"]), int(gd["y"]), int(gd["vx"]), int(gd["vy"])))
        return robots

    def solve(self) -> None:
        print("solving...")
        # found the following pattern with similar looking images:
        # 99 -> 200 -> 301 -> 402

        # following the pattern with this code
        # self.steps: int = 99
        # while True:
        #     self.do_the_robot()
        #     input(f"<steps: {self.steps} enter to continue>")
        #     self.steps += 101

        # resulted in this answer
        self.steps: int = 8280
        self.result = self.steps
        # uncomment to see the image
        # self.do_the_robot()

    def do_the_robot(self):
        final_pos: list[Pos] = []
        for robot in self.get_robots():
            # calculate the final resting place of the robots using speed, steps and initial position
            final_x: int = (robot.vx * self.steps + robot.x) % self.width
            final_y: int = (robot.vy * self.steps + robot.y) % self.height
            # add the robot to the robot pile
            final_pos.append(Pos(final_x, final_y))
        # print the robots
        for y in range(self.height):
            for x in range(self.width):
                if Pos(x, y) in final_pos:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
