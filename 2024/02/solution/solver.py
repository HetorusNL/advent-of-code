from pathlib import Path

from solution.part1 import Part1
from solution.part2 import Part2


class Solver:
    def __init__(self):
        # construct the path to the input_files for this day
        this_folder: Path = Path(__file__).parent
        input_files_folder: Path = (this_folder / ".." / "input_files").resolve()
        # check whether we have 1 or 2 input files (e.g. reuse or different input for the two parts)
        input_files: list[Path] = list(filter(lambda file: file.name.endswith(".txt"), input_files_folder.iterdir()))
        assert len(input_files) in [1, 2], f"found {len(input_files)} input files, we only support 1 or 2!"
        if len(input_files) == 1:
            self.part1: Part1 = Part1(input_files[0])
            self.part2: Part2 = Part2(input_files[0])
        else:
            # we assume that the input files are sorted
            self.part1: Part1 = Part1(input_files[0])
            self.part2: Part2 = Part2(input_files[1])

    def solve(self):
        # solve and display the result of part 1
        print("solving part 1")
        self.part1.solve()
        print("result of part 1 is:")
        print(self.part1.get_result())

        # solve and display the result of part 2
        print("\nsolving part 2")
        self.part2.solve()
        print("result of part 2 is:")
        print(self.part2.get_result())
