from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        assert len(self.lines) == 1

    def blink(self) -> None:
        index: int = 0
        while index < len(self.stones):
            if self.stones[index] == 0:
                # if 0, replace with 1
                self.stones[index] = 1
            elif len(str(self.stones[index])) % 2 == 0:
                # if even num digits, split in 2 even sized new stones
                length: int = len(str(self.stones[index])) // 2
                first: str = str(self.stones[index])[:length]
                second: str = str(self.stones[index])[length:]
                self.stones[index] = int(first)
                self.stones.insert(index + 1, int(second))
                index += 1
            else:
                # multiply by 2024
                self.stones[index] *= 2024
            index += 1

    def solve(self) -> None:
        print("solving...")
        self.stones: list[int] = list(map(int, self.lines[0].split()))
        for _ in range(25):
            self.blink()
        self.result = len(self.stones)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
