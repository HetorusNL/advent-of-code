import math
from pathlib import Path

from solution.chamber import Chamber


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.line = f.readline().strip()

    def solve(self) -> None:
        print("solving...")
        print("...taking roughly 20 minutes...")
        chamber_repeat = Chamber(self.line)
        # calculate the least common multiple of the wind and the rock types
        least_common_multiple = math.lcm(len(self.line), chamber_repeat.num_different_rocks)
        print(f"running two times sequence_length simulations of {least_common_multiple} rocks")
        # simulate least_common_multiple a number of times and guess estimate the sequence length
        sequence: list[int] = []
        prev_tower_height = 0
        simulation_run = 0
        while True:
            simulation_run += 1
            print(".", end="", flush=True)
            for _ in range(least_common_multiple):
                chamber_repeat.fall_rock()
            chamber_repeat.optimize()
            sequence.append(chamber_repeat.tower_height - prev_tower_height)
            prev_tower_height = chamber_repeat.tower_height
            try:
                sequence_length = self._get_sequence_length(sequence[1:])
                break  # found the sequence length, stop the loop
            except AssertionError:
                pass
        print()
        # calculate the sequence length (removing first element as it is different)
        repeats_after = sequence_length * least_common_multiple
        tower_initial_repeat_height = sum(sequence[:sequence_length])
        tower_height_for_repeat = sum(sequence[sequence_length : 2 * sequence_length])

        # calculate repeates for target
        target = 1000000000000
        # remove the first 'repeats_after' rocks from the target
        target -= repeats_after
        num_repeats = target // repeats_after
        remaining_rocks = target % repeats_after

        # simulate remaining rocks
        print(f"running {repeats_after} + {remaining_rocks} more simulations")
        # prep the chamber by running the first sequence
        chamber_remaining = Chamber(self.line)
        simulation_run = 0
        for i in range(repeats_after):
            chamber_remaining.fall_rock()
            if i % least_common_multiple == 0:
                simulation_run += 1
                print(".", end="", flush=True)
                chamber_remaining.optimize()
        chamber_remaining_initial_height = chamber_remaining.tower_height
        # simulate the remaining number of rocks
        for i in range(remaining_rocks):
            chamber_remaining.fall_rock()
            if i % least_common_multiple == 0:
                simulation_run += 1
                print(".", end="", flush=True)
                chamber_remaining.optimize()
        print()
        tower_height_remaining_rocks = chamber_remaining.tower_height - chamber_remaining_initial_height

        # calculate the total tower height
        self.tower_height = (
            tower_initial_repeat_height + tower_height_for_repeat * num_repeats + tower_height_remaining_rocks
        )

    def _get_sequence_length(self, sequence: list[int]) -> int:
        for i in range(2, len(sequence) // 2):
            if sequence[0:i] == sequence[i : 2 * i]:
                return i
        raise AssertionError("no sequence length found!")

    def get_result(self) -> str:
        return f"the height of the rock tower after 1000000000000 rocks is: {self.tower_height}"
