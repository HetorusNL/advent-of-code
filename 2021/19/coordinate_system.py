from coord import Coord


class CoordinateSystem:
    def __init__(self):
        self.coordinate_systems = [
            ["x", "y", "z"],
            ["x", "y", "-z"],
            ["x", "-y", "z"],
            ["x", "-y", "-z"],
            ["x", "z", "y"],
            ["x", "z", "-y"],
            ["x", "-z", "y"],
            ["x", "-z", "-y"],
            ["-x", "y", "z"],
            ["-x", "y", "-z"],
            ["-x", "-y", "z"],
            ["-x", "-y", "-z"],
            ["-x", "z", "y"],
            ["-x", "z", "-y"],
            ["-x", "-z", "y"],
            ["-x", "-z", "-y"],
            ["y", "x", "z"],
            ["y", "x", "-z"],
            ["y", "-x", "z"],
            ["y", "-x", "-z"],
            ["y", "z", "x"],
            ["y", "z", "-x"],
            ["y", "-z", "x"],
            ["y", "-z", "-x"],
            ["-y", "x", "z"],
            ["-y", "x", "-z"],
            ["-y", "-x", "z"],
            ["-y", "-x", "-z"],
            ["-y", "z", "x"],
            ["-y", "z", "-x"],
            ["-y", "-z", "x"],
            ["-y", "-z", "-x"],
            ["z", "y", "x"],
            ["z", "y", "-x"],
            ["z", "-y", "x"],
            ["z", "-y", "-x"],
            ["z", "x", "y"],
            ["z", "x", "-y"],
            ["z", "-x", "y"],
            ["z", "-x", "-y"],
            ["-z", "y", "x"],
            ["-z", "y", "-x"],
            ["-z", "-y", "x"],
            ["-z", "-y", "-x"],
            ["-z", "x", "y"],
            ["-z", "x", "-y"],
            ["-z", "-x", "y"],
            ["-z", "-x", "-y"],
        ]
        self.system = 0

    def next(self):
        """selects the next coordinate system, returns 0 on overflow"""
        self.system = (self.system + 1) % len(self.coordinate_systems)
        return self.system == 0

    def reset(self):
        """resets the coordinate system to [x, y, z]"""
        self.system = 0

    def apply(self, coord: Coord):
        """applies coordinate system transformation and returns new Coord"""
        coord_system = self.coordinate_systems[self.system]
        new_coord_values = []
        for i in range(len(coord_system)):
            if "x" in coord_system[i]:
                new_val = coord.x
            elif "y" in coord_system[i]:
                new_val = coord.y
            elif "z" in coord_system[i]:
                new_val = coord.z
            else:
                assert False  # found an illegal coordinate
            if "-" in coord_system[i]:
                new_val = -new_val
            new_coord_values.append(new_val)
        return Coord(new_coord_values)
