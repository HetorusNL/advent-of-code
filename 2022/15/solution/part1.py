from pathlib import Path
from typing import Union

from solution.sensor import Sensor


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        sensors: list[Sensor] = [Sensor(line) for line in self.lines]
        # get the sensor range for the target row
        target_row: int = 2000000
        sensor_ranges: list[Union[tuple[int, int], None]] = [
            sensor.get_range_for_row(target_row) for sensor in sensors
        ]
        # filter out out-of-range sensors and sort
        sensor_ranges_in_range: list[tuple[int, int]] = sorted(
            sensor_range for sensor_range in sensor_ranges if sensor_range
        )
        self.positions: int = 0
        current_range, *sensor_ranges_in_range = sensor_ranges_in_range
        current_range: tuple[int, int]
        while sensor_ranges_in_range:
            new_range, *sensor_ranges_in_range = sensor_ranges_in_range
            new_range: tuple[int, int]
            # test if new in current
            if new_range[0] >= current_range[0] and new_range[1] <= current_range[1]:
                # don't process new_range, as it's already in current range
                pass
            # test if overlapping
            elif new_range[0] <= current_range[1]:
                # enlarge the current range
                current_range: tuple[int, int] = current_range[0], new_range[1]
            # otherwise it's non-overlapping
            else:
                # add positions and set new current range
                self.positions += current_range[1] - current_range[0] + 1
                current_range: tuple[int, int] = new_range
        # add the ramaining range to the positions
        self.positions += current_range[1] - current_range[0] + 1

        # remove the beacons in the row
        self.positions -= len(set(sensor._beacon_x for sensor in sensors if sensor._beacon_y == target_row))

    def get_result(self) -> str:
        return f"the number of positions a beacon can't exist is: {self.positions}"
