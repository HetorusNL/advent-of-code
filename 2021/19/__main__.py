from coord import Coord
from scanner import Scanner
import re
from typing import List


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            lines = [line.strip() for line in f.readlines()]

        self.scanners: List[Scanner] = []

        i = 0
        while i < len(lines):
            # wait for new scanner line
            match = re.match(r"--- scanner (?P<scanner>[0-9]*) ---", lines[i])
            if match:
                # found a scanner, create a new scanner
                new_scanner = Scanner(match.groupdict()["scanner"])
                i += 1
                # check if all lines are read
                while i < len(lines):
                    # it line matches a coordinate, extract and add to scanner
                    if re.match(r"[\-0-9]*,[\-0-9]*,[\-0-9]*", lines[i]):
                        coord = Coord(lines[i])
                        new_scanner.add_coord(coord)
                    else:
                        break
                    i += 1
                self.scanners.append(new_scanner)
            i += 1

    def solve(self):
        self.part_1()
        self.part_2()

    def part_1(self):
        # process all scanners relative to the first one
        print("resolving all scanners, this will take a while...")
        master_scanner = self.scanners[0]
        scanners_left = self.scanners[1:]
        i = 0
        while scanners_left and i < len(scanners_left):
            if self._process_scanner(master_scanner, scanners_left[i]):
                scanners_left.remove(scanners_left[i])
                if i != 0:
                    print()
                print(f"scanners left: {len(scanners_left)}", flush=True)
                i = 0
            else:
                print("-", end="", flush=True)
                i += 1
        num_beacons = len(master_scanner.coords)
        print(f"number of beacons: {num_beacons}")

    def part_2(self):
        max_distance = 0
        for left in range(len(self.scanners)):
            for right in range(len(self.scanners)):
                if left == right:
                    continue
                left_offsets = self.scanners[left].coord_offset.values()
                right_offsets = self.scanners[right].coord_offset.values()
                dist = 0
                for axis in range(3):
                    dist += abs(left_offsets[axis] - right_offsets[axis])
                max_distance = max(max_distance, dist)
        print(f"max distance between any two scanners: {max_distance}")

    def _process_scanner(self, base: Scanner, relative: Scanner):
        # find all distances for all coordinate transforms for all coords
        relative.coordinate_system.reset()
        i = 0
        while True:
            i += 1
            distances = {}
            offsets = {}
            for coord in relative.get_coords():
                for base_coord in base.get_coords():
                    distance = base_coord - coord
                    # store distance in string form in a dictionary
                    values = str(distance.values())
                    if values not in distances.keys():
                        distances[values] = 0
                        offsets[values] = distance
                    distances[values] += 1
            if distances[max(distances, key=distances.get)] >= 12:
                # print("found coord system and transformation!")
                offset = offsets[max(distances, key=distances.get)]
                # print(f"offset: {offset.values()}")
                relative.coord_offset = offset
                # add the coords not present in base in relative:
                for coord in relative.get_coords():
                    base.add_coord(coord)
                # print(f"successfully processed scanner {relative.scanner}")
                return True
            if relative.coordinate_system.next():
                # print(f"failed to process scanner {relative.scanner}")
                return False


if __name__ == "__main__":
    Solution().solve()
