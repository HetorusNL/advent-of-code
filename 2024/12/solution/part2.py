from enum import auto
from enum import Enum
from pathlib import Path


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def get_plot(self, x: int, y: int) -> str | None:
        # return None when we're outside of the garden
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        # otherwise return the str at that location
        return self.lines[self.height - y - 1][x]

    def process(self, x: int, y: int, plant_dict: dict[int, dict[int, bool]]):
        self.processed[x][y] = True
        if x not in plant_dict:
            plant_dict[x] = {}
        plant_dict[x][y] = True

    def flood_fill(self, x: int, y: int, plant: str, plant_dict: dict[int, dict[int, bool]]):
        self.process(x, y, plant_dict)
        if self.get_plot(x - 1, y) == plant:
            if not self.processed[x - 1][y]:
                self.flood_fill(x - 1, y, plant, plant_dict)
        if self.get_plot(x + 1, y) == plant:
            if not self.processed[x + 1][y]:
                self.flood_fill(x + 1, y, plant, plant_dict)
        if self.get_plot(x, y - 1) == plant:
            if not self.processed[x][y - 1]:
                self.flood_fill(x, y - 1, plant, plant_dict)
        if self.get_plot(x, y + 1) == plant:
            if not self.processed[x][y + 1]:
                self.flood_fill(x, y + 1, plant, plant_dict)

    def add_fence(self, x: int, y: int, fence: dict[int, dict[int, bool]]):
        if x not in fence:
            fence[x] = {}
        fence[x][y] = True

    def process_horizontal_fence(self, horizontal_fence: dict[int, dict[int, bool]]) -> int:
        # count horizontal continuous segments in the provided dictionary
        fence: int = 0
        for y in range(self.height + 1):
            found_fence = False
            for x in range(self.width):
                if horizontal_fence.get(x, {}).get(y):
                    if not found_fence:
                        found_fence = True
                        fence += 1
                else:
                    found_fence = False
        return fence

    def process_vertical_fence(self, vertical_fence: dict[int, dict[int, bool]]) -> int:
        # count vertical continuous segments in the provided dictionary
        fence: int = 0
        for x in range(self.width + 1):
            found_fence = False
            for y in range(self.height):
                if vertical_fence.get(x, {}).get(y):
                    if not found_fence:
                        found_fence = True
                        fence += 1
                else:
                    found_fence = False
        return fence

    def process_fill(self, plant_dict: dict[int, dict[int, bool]]) -> int:
        area: int = 0
        fence: int = 0
        left_fence: dict[int, dict[int, bool]] = {}
        right_fence: dict[int, dict[int, bool]] = {}
        up_fence: dict[int, dict[int, bool]] = {}
        down_fence: dict[int, dict[int, bool]] = {}
        for x, row_y in plant_dict.items():
            for y in row_y.keys():
                # add one to the area for every plot
                area += 1
                # test for every edge if there is a same plant
                if not plant_dict.get(x - 1, {}).get(y):
                    self.add_fence(x, y, left_fence)
                if not plant_dict.get(x + 1, {}).get(y):
                    self.add_fence(x, y, right_fence)
                if not plant_dict.get(x, {}).get(y - 1):
                    self.add_fence(x, y, down_fence)
                if not plant_dict.get(x, {}).get(y + 1):
                    self.add_fence(x, y, up_fence)
        # process horizontal fences
        fence += self.process_horizontal_fence(up_fence)
        fence += self.process_horizontal_fence(down_fence)
        # process vertical fences
        fence += self.process_vertical_fence(left_fence)
        fence += self.process_vertical_fence(right_fence)
        return area * fence

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        # pre-fill the processed dict
        self.processed: dict[int, dict[int, bool]] = {}
        for x in range(self.width):
            self.processed[x] = {}
            for y in range(self.height):
                self.processed[x][y] = False
        # loop through all plots in the garden
        for x in range(self.width):
            for y in range(self.height):
                if not self.processed[x][y]:
                    plant = self.get_plot(x, y)
                    assert plant
                    plant_dict: dict[int, dict[int, bool]] = {}
                    self.flood_fill(x, y, plant, plant_dict)
                    self.result += self.process_fill(plant_dict)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
