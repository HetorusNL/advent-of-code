from cave import Cave
from typing import List


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            self._cave_names = [l.strip().split("-") for l in f.readlines()]
            self._unique_caves = []
            [self._unique_caves.extend(name) for name in self._cave_names]
            self._unique_caves = list(set(self._unique_caves))

        self._caves = [Cave(name) for name in self._unique_caves]
        for cave in self._caves:
            cave.resolve(self._cave_names, self._caves)

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        visit_func = lambda cave, adj_c, path: cave.can_visit1(adj_c, path)
        paths = self._run(visit_func)
        print(f"number of paths with small caves visited once: {paths}")

    def part_2(self):
        visit_func = lambda cave, adj_c, path: cave.can_visit2(adj_c, path)
        paths = self._run(visit_func)
        print(f"number of paths with 1 small caves visited twice: {paths}")

    def _run(self, visit_func):
        start_cave = [cave for cave in self._caves if cave.name == "start"][0]
        self._paths = []
        self._path = [start_cave]
        self._recurse(start_cave, visit_func)
        return len(self._paths)

    def _recurse(self, cave: Cave, visit_func):
        for adjacent_cave in cave.adjacent_caves:
            can_visit = visit_func(cave, adjacent_cave, self._path)
            self._path.append(adjacent_cave)
            if adjacent_cave.name == "end":
                self._paths.append([cave.name for cave in self._path])
            elif can_visit:
                self._recurse(adjacent_cave, visit_func)
            self._path.pop()


if __name__ == "__main__":
    Solution().solve()
