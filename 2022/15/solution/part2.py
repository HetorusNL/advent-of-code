from pathlib import Path
from typing import Union
from multiprocessing.pool import Pool

from solution.sensor import Sensor


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        print("...taking roughly 9 seconds...")
        self.sensors: list[Sensor] = [Sensor(line) for line in self.lines]
        self.max_pos = 4000000
        # use a process pool to extract the answer of all max_pos rows
        self.beacon_tuning_frequency = list(
            filter(lambda result: result, Pool().map(self._solve_row, range(0, self.max_pos + 1, 100)))
        )[0]

    def _solve_row(self, start_row):
        for target_row in range(start_row, min(self.max_pos, start_row + 100)):
            # get the sensor range for the target row
            sensor_ranges: list[Union[tuple[int, int], None]] = [
                sensor.get_range_for_row(target_row) for sensor in self.sensors
            ]
            # filter out out-of-range sensors and sort
            end_pos: int = -1
            for sensor_range in sorted(sensor_range for sensor_range in sensor_ranges if sensor_range):
                # test if we found our beacon location, set tuning frequency and return
                if sensor_range[0] > end_pos:
                    return self.max_pos * (end_pos + 1) + target_row
                # we're outside of our beacon range, continue
                if sensor_range[1] > self.max_pos:
                    break
                # otherwise update the end_pos
                end_pos = max(end_pos, sensor_range[1])

    def get_result(self) -> str:
        return f"the beacon tuning frequency is: {self.beacon_tuning_frequency}"
