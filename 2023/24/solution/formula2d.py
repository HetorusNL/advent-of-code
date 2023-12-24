class Formula2D:
    def __init__(self, x: int, y: int, vx: int, vy: int):
        # y = ax + b
        a = vy / vx
        b = y - a * x
        self.a = a
        self.b = b
