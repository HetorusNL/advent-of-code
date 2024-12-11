from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        assert len(self.lines) == 1

    def blink(self, stone: int) -> list[int]:
        if stone == 0:
            # if 0, replace with 1
            return [1]
        elif len(str(stone)) % 2 == 0:
            # if even num digits, split in 2 even sized new stones
            length: int = len(str(stone)) // 2
            first: str = str(stone)[:length]
            second: str = str(stone)[length:]
            return [int(first), int(second)]
        else:
            # multiply by 2024
            return [stone * 2024]

    def blink_dict(self, stones: dict[int, int]):
        # store stone_value and count of stone values in a dict
        new_stones: dict[int, int] = {}
        for stone, num_stones in stones.items():
            stones_after_blink = self.blink(stone)
            for new_stone in stones_after_blink:
                if new_stone not in new_stones:
                    # add new entry in the stones dict with num_stones
                    new_stones[new_stone] = num_stones
                else:
                    # add num_stones to the dict
                    new_stones[new_stone] += num_stones
        return new_stones

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        stones: list[int] = list(map(int, self.lines[0].split()))
        stones_dict: dict[int, int] = {stone: 1 for stone in stones}
        for _ in range(75):
            stones_dict = self.blink_dict(stones_dict)
        self.result = sum(stones_dict.values())

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
