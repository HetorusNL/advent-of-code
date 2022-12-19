import math
from pathlib import Path

from solution.chamber import Chamber


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.line = f.readline().strip()

        # self.line = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

    def solve(self) -> None:
        print("solving...")
        chamber_repeat = Chamber(self.line)
        # calculate the least common multiple of the wind and the rock types
        least_common_multiple = math.lcm(len(self.line), chamber_repeat.num_different_rocks)
        print(least_common_multiple)
        # simulate least_common_multiple a number of times and guess estimate the sequence length
        sequence: list[int] = []
        prev_tower_height = 0
        simulation_run = 0
        while True:
            simulation_run += 1
            print(simulation_run)
            for _ in range(least_common_multiple):
                chamber_repeat.fall_rock()
            sequence.append(chamber_repeat.tower_height - prev_tower_height)
            prev_tower_height = chamber_repeat.tower_height
            try:
                if len(sequence) % 10 == 0:
                    print(sequence)
                sequence_length = self._get_sequence_length(sequence[1:])
                break  # found the sequence length, stop the loop
            except AssertionError:
                pass
        del chamber_repeat
        # calculate the sequence length (removing first element as it is different)
        print(sequence)
        repeats_after = sequence_length * least_common_multiple
        tower_initial_repeat_height = sum(sequence[:sequence_length])
        tower_height_for_repeat = sum(sequence[sequence_length : 2 * sequence_length])
        print(sequence_length)
        print(tower_height_for_repeat)

        # calculate repeates for target
        target = 1000000000000
        # remove the first 'sequence_length' rocks from the target
        target -= repeats_after
        num_repeats = target // repeats_after
        print(num_repeats)
        remaining_rocks = target % num_repeats
        print("remaining", remaining_rocks)

        # simulate remaining rocks
        # prep the chamber by running the first sequence
        chamber_remaining = Chamber(self.line)
        for _ in range(repeats_after):
            chamber_remaining.fall_rock()
        chamber_remaining_initial_height = chamber_remaining.tower_height
        # simulate the remaining number of rocks
        for _ in range(remaining_rocks):
            chamber_remaining.fall_rock()
        tower_height_remaining_rocks = chamber_remaining.tower_height - chamber_remaining_initial_height

        # calculate the total tower height
        print(tower_initial_repeat_height, tower_height_for_repeat, num_repeats, tower_height_remaining_rocks)
        self.tower_height = (
            tower_initial_repeat_height + tower_height_for_repeat * num_repeats + tower_height_remaining_rocks
        )

    def _pos_x_equal(self, pos1: list[list[int]], pos2: list[list[int]]) -> bool:
        assert len(pos1) == len(pos2)
        for i in range(len(pos1)):
            if pos1[i][0] != pos2[i][0]:
                return False
        return True

    def _get_sequence_length(self, sequence: list[int]) -> int:
        for i in range(2, len(sequence) // 2):
            if sequence[0:i] == sequence[i : 2 * i]:
                return i
        raise AssertionError("no sequence length found!")

    def get_result(self) -> str:
        return f"the height of the rock tower after 1000000000000 rocks is: {self.tower_height}"
