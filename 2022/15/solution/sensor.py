import re
from typing import Union


class Sensor:
    def __init__(self, line: str):
        # parse the regex input line
        regex = r"Sensor at x=(?P<sensor_x>[0-9-]*), y=(?P<sensor_y>[0-9-]*): "
        regex += r"closest beacon is at x=(?P<beacon_x>[0-9-]*), y=(?P<beacon_y>[0-9-]*)"
        match = re.match(regex, line)
        assert match, f"regex is not a match for {line}!"
        # store the properties in the class
        self._sensor_x = int(match["sensor_x"])
        self._sensor_y = int(match["sensor_y"])
        self._beacon_x = int(match["beacon_x"])
        self._beacon_y = int(match["beacon_y"])
        self._distance_x = abs(self._sensor_x - self._beacon_x)
        self._distance_y = abs(self._sensor_y - self._beacon_y)
        self._manhattan_distance = self._distance_x + self._distance_y

    def get_range_for_row(self, row: int) -> Union[tuple[int, int], None]:
        distance_left = self._manhattan_distance - abs(self._sensor_y - row)
        if distance_left < 0:
            return None
        return self._sensor_x - distance_left, self._sensor_x + distance_left
