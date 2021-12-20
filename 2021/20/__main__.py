from image import Image


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            lines = [line.strip() for line in f.readlines()]

        self.image = Image()
        self.image.set_image_processing_algorithm(lines[0])

        for y in range(len(lines[2:])):
            for x in range(len(lines[y + 2])):
                self.image.add_pixel(x, y, lines[y + 2][x])

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        for _ in range(2):
            self.image.apply_algorithm()
        pixels_lit = self.image.count_pixels()
        print(f"pixels lit in the 2 times enhanced image: {pixels_lit}")

    def part_2(self):
        for _ in range(50):
            self.image.apply_algorithm()
        pixels_lit = self.image.count_pixels()
        print(f"pixels lit in the 50 times enhanced image: {pixels_lit}")


if __name__ == "__main__":
    Solution().solve()
