from pathlib import Path
import random


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def get_label_index(self, label: str):
        if label not in self.labels:
            self.labels.append(label)
        return self.labels.index(label)

    def solve(self) -> None:
        print("solving...")
        self.result = 42
        self.connections: list[tuple[int, int]] = []
        self.labels: list[str] = []
        self.do_magic()

    def do_magic(self):
        self.V: set[str | tuple[str]] = set()
        self.E: set[str | tuple[str, str]] = set()
        for line in self.lines:
            v, *ws = line.replace(":", " ").split()
            self.V |= {v, *ws}
            self.E |= {(v, w) for w in ws}

        parts = self.min_cut()
        self.result = parts[0] * parts[1]

    def min_cut(self):
        ss = lambda v: next(s for s in subsets if v in s)
        while True:
            subsets = [{v} for v in self.V]

            while len(subsets) > 2:
                s1, s2 = map(ss, random.choice([*self.E]))
                if s1 != s2:
                    s1 |= s2
                    subsets.remove(s2)
            if sum(ss(u) != ss(v) for u, v in self.E) < 4:
                break
        return list(map(len, subsets))

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
