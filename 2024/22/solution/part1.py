from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def evolve_secret(self, previous: int) -> int:
        # step 1
        secret: int = ((previous * 64) ^ previous) % 16777216
        # step 2
        secret = ((secret // 32) ^ secret) % 16777216
        # step 3
        secret = ((secret * 2048) ^ secret) % 16777216
        # return the new secret
        return secret

    def solve(self) -> None:
        print("solving...")
        self.result: int = 0
        for line in self.lines:
            secret = int(line)
            for _ in range(2000):
                secret = self.evolve_secret(secret)
            self.result += secret

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
