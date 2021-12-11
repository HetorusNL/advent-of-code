class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """implements 'Coord(..) in [..]' (Coord in list) functionality"""
        return self.x == other.x and self.y == other.y

    def adjacent_coords(self, w, h):
        """returns (horizontal, vertical and diagonal) adjacent coordinates"""
        # syntactical sugar for adjacent_coords_hvd
        return self.adjacent_coords_hvd(w, h)

    def adjacent_coords_hvd(self, w, h):
        """returns horizontal, vertical and diagonal adjacent coordinates"""
        ac = self.adjacent_coords_hv(w, h)
        if self.x > 0 and self.y > 0:
            ac.append(Coord(self.x - 1, self.y - 1))
        if self.x > 0 and self.y < (h - 1):
            ac.append(Coord(self.x - 1, self.y + 1))
        if self.x < (w - 1) and self.y > 0:
            ac.append(Coord(self.x + 1, self.y - 1))
        if self.x < (w - 1) and self.y < (h - 1):
            ac.append(Coord(self.x + 1, self.y + 1))
        return ac

    def adjacent_coords_hv(self, w, h):
        """returns horizontal and vertical adjacent coordinates"""
        ac = []
        if self.x > 0:
            ac.append(Coord(self.x - 1, self.y))
        if self.x < (w - 1):
            ac.append(Coord(self.x + 1, self.y))
        if self.y > 0:
            ac.append(Coord(self.x, self.y - 1))
        if self.y < (h - 1):
            ac.append(Coord(self.x, self.y + 1))
        return ac
