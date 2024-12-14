from pathlib import Path
import re


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


class Part1:
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
        top_left: int = 0
        top_right: int = 0
        bottom_left: int = 0
        bottom_right: int = 0
        for robot in self.get_robots():
            # calculate the final resting place of the robots using speed, steps and initial position
            final_x: int = (robot.vx * self.steps + robot.x) % self.width
            final_y: int = (robot.vy * self.steps + robot.y) % self.height
            # check if the robot corresponds to one of the 4 quadrants
            if final_x < self.width // 2 and final_y < self.height // 2:
                top_left += 1
            if final_x > self.width // 2 and final_y < self.height // 2:
                top_right += 1
            if final_x < self.width // 2 and final_y > self.height // 2:
                bottom_left += 1
            if final_x > self.width // 2 and final_y > self.height // 2:
                bottom_right += 1
        self.result = top_left * top_right * bottom_left * bottom_right

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
