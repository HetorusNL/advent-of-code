class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        self._dots = []
        self._fold_along = []
        with open("input.txt") as f:
            lines = f.readlines()
        coords = []
        for line in lines:
            line.strip()
            if "," in line:
                coords.append([int(i) for i in line.split(",")])
            if "fold along" in line:
                self._fold_along.append([line[11:12], int(line[13:])])
        self._w = max(coord[0] for coord in coords) + 1
        self._h = max(coord[1] for coord in coords) + 1
        [self._dots.append([0] * self._w) for _ in range(self._h)]
        for x, y in coords:
            self._dots[y][x] = 1

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        self._fold(self._fold_along[0])
        visible_dots = self._visible_dots()
        print(f"visible dots after the first fold instruction: {visible_dots}")

    def part_2(self):
        for fold in self._fold_along:
            self._fold(fold)
        print("code to activate the infrared thermal imaging camera system:")
        self._print()  # LKREBPRK

    def _fold(self, fold_along):
        if fold_along[0] == "x":
            fold_line = self._w // 2
            for y in range(self._h):
                for x in range(fold_line + 1):
                    self._dots[y][x] += self._dots[y][self._w - x - 1]
            self._w = self._w // 2
        else:  # fold_along[0] == "y"
            fold_line = self._h // 2
            for y in range(fold_line + 1):
                for x in range(self._w):
                    self._dots[y][x] += self._dots[self._h - y - 1][x]
            self._h = self._h // 2

    def _visible_dots(self):
        v_dots = 0
        for y in range(self._h):
            v_dots += sum([1 if x else 0 for x in self._dots[y][0 : self._w]])
        return v_dots

    def _print(self):
        for line in self._dots[0 : self._h]:
            print("".join(["#" if c else "." for c in line[0 : self._w]]))


if __name__ == "__main__":
    Solution().solve()
