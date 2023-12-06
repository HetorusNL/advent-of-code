from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.times = list(map(int, [line for line in self.lines[0].split(" ")[1:] if line]))
        self.distances = list(map(int, [line for line in self.lines[1].split(" ")[1:] if line]))

    def solve(self) -> None:
        print("solving...")
        race_wins = {}
        for race in range(len(self.times)):
            race_wins[race] = 0
            race_time = self.times[race]
            race_distance = self.distances[race]
            for charge_time in range(self.times[race]):
                distance = (race_time - charge_time) * charge_time
                if distance > race_distance:
                    race_wins[race] += 1
        self.result = 1
        for num_race_wins in race_wins.values():
            self.result *= num_race_wins

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
