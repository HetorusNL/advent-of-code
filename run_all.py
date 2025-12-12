import subprocess
from pathlib import Path
from time import time_ns


class AoCRunner:
    def __init__(self):
        self.YEAR: str = "2025"
        self.test_failed: bool = False
        self.index: int = 0
        self.solutions: list[str] = []
        self.correct_solutions: list[str] = [
            "Day 01 Part 1: [solution] the number of rotations that end in zero are: 1059",
            "Day 01 Part 2: [solution] the number of rotations that end in zero are: 6305",
            "Day 02 Part 1: [solution] result: 20223751480",
            "Day 02 Part 2: [solution] result: 30260171216",
            "Day 03 Part 1: [solution] total joltage: 17244",
            "Day 03 Part 2: [solution] total joltage: 171435596092638",
            "Day 04 Part 1: [solution] accessible rolls: 1437",
            "Day 04 Part 2: [solution] accessible rolls: 8765",
            "Day 05 Part 1: [solution] number of fresh ingredients: 529",
            "Day 05 Part 2: [solution] total number of fresh ingredients in the ranges: 344260049617193",
            "Day 06 Part 1: [solution] the grand total to the individual problems is 5595593539811",
            "Day 06 Part 2: [solution] the grand total to the individual problems is 10153315705125",
            "Day 07 Part 1: [solution] the number of beam splits in the tachyon manifold is: 1579",
            "Day 07 Part 2: [solution] the number of timelines of a single tachyon particle is: 13418215871354",
            "Day 08 Part 1: [solution] the largest 3 circuit sizes multiplied togeter: 102816",
            "Day 08 Part 2: [solution] the x coordinate of the last to points multiplied togeter: 100011612",
            "Day 09 Part 1: [solution] largest area of any rectangle: 4754955192",
            "Day 09 Part 2: [solution] largest area of any rectangle using only red and green tiles: 1568849600",
            "Day 10 Part 1: [solution] fewest button presses to configure the indicators: 532",
            "Day 10 Part 2: [solution] fewest button presses to configure the indicators: NOT_FINISHED",
            "Day 11 Part 1: [solution] paths from you to out: 423",
            "Day 11 Part 2: [solution] paths from svr via dac_fft to out: 333657640517376",
        ]
        self.run()

    def run_part(self, day: str, part: int) -> None:
        start: int = time_ns()
        result = subprocess.run(
            f"uv run -m tapl.src.compilers.compyler {self.YEAR}/{day}/part{part}.tim",
            shell=True,
            capture_output=True,
            text=True,
        )
        duration: int = time_ns() - start
        lines = result.stdout.strip().split("\n")
        solution: str = ""
        for line in lines:
            # show the compiler errors
            if "error:" in line:
                print(line)
            # process the solution line
            if line.startswith("[solution]"):
                time: str = f"{(int(duration//1e9))}.{int((duration//1e6)%1e3):03d}s"
                print(f"Day {day} Part {part}: [{time}] {line}")
                solution = f"Day {day} Part {part}: {line}"
        if len(self.correct_solutions) > self.index:
            correct_solution: str = self.correct_solutions[self.index]
            if solution != correct_solution:
                self.test_failed = True
                print(f"error verifying solution!")
                print(f"correct solution:    '{correct_solution}'")
                print(f"calculated solution: '{solution}'\n")
        else:
            print(f"no correct solution to verify against for Day {day} Part {part}\n")
        self.index += 1

    def run(self):
        # Find all day folders in 2025 directory
        year_path = Path(self.YEAR)
        day_folders = sorted([d for d in year_path.iterdir() if d.is_dir() and d.name.isdigit()])

        for day_folder in day_folders:
            day: str = day_folder.name
            self.run_part(day, 1)
            self.run_part(day, 2)

        exit(1 if self.test_failed else 0)


if __name__ == "__main__":
    AoCRunner()
