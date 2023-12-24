from solution.formula2d import Formula2D
from solution.pos2d import Pos2D


class Hailstone:
    def __init__(self, line: str):
        pos, velocity = line.split("@")
        self.x, self.y, self.z = [int(pos) for pos in pos.split(",")]
        self.vx, self.vy, self.vz = [int(vel) for vel in velocity.split(",")]
        self.formula_2d = Formula2D(self.x, self.y, self.vx, self.vy)

    def intersects_in_bounds(self, other: "Hailstone", min_value: int, max_value: int) -> bool:
        intersection = self.intersects(other)
        # lines run parallel
        if not intersection:
            return False
        # otherwise check if the intersection happened before the pos of the hailstones
        if self.intersection_in_past(self, intersection):
            return False
        if self.intersection_in_past(other, intersection):
            return False
        # then check if the Pos2D values are within min and max
        if intersection.x < min_value or intersection.x > max_value:
            return False
        if intersection.y < min_value or intersection.y > max_value:
            return False
        return True

    def intersection_in_past(self, hailstone: "Hailstone", intersection: Pos2D):
        if hailstone.vx > 0:
            if intersection.x < hailstone.x:
                return True
        else:
            if intersection.x > hailstone.x:
                return True
        return False

    def intersects(self, other: "Hailstone") -> Pos2D | None:
        if self.formula_2d.a == other.formula_2d.a:
            return None
        # shorthands for the formulas
        f1 = self.formula_2d
        f2 = other.formula_2d
        # x = (b2 - b1) / (a1 - a2)
        x = (f2.b - f1.b) / (f1.a - f2.a)
        # y = ax + b
        y = f1.a * x + f1.b
        return Pos2D(x, y)

    def __repr__(self) -> str:
        return f"x=[{self.x},{self.y},{self.z}] v=[{self.vx},{self.vy},{self.vz}]"
