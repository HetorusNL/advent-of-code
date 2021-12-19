from coord import Coord
from coordinate_system import CoordinateSystem
from typing import List


class Scanner:
    def __init__(self, scanner):
        self.scanner = scanner
        self.coords: List[Coord] = []
        self.coord_offset = Coord()
        self.coordinate_system = CoordinateSystem()

    def __eq__(self, other):
        return id(self) == id(other)

    def add_coord(self, coord: Coord):
        if coord not in self.coords:
            self.coords.append(coord)

    def get_coords(self):
        # async return the coords with coordinal system and relative offset
        for coord in self.coords:
            yield self.coordinate_system.apply(coord) + self.coord_offset
