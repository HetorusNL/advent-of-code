class Node:
    def __init__(self, x, y, w, h, _map):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._map = _map
        self.visited = False
        self.distance = float("inf")

    def adjacent_nodes(self):
        """returns (horizontal, vertical and diagonal) adjacent coordinates"""
        # syntactical sugar for adjacent_nodes_hvd
        return self.adjacent_nodes_hvd()

    def adjacent_nodes_hvd(self):
        """returns horizontal, vertical and diagonal adjacent coordinates"""
        ac = self.adjacent_nodes_hv(self.w, self.h)
        if self.x > 0 and self.y > 0:
            ac.append(self._map[self.x - 1][self.y - 1])
        if self.x > 0 and self.y < (self.h - 1):
            ac.append(self._map[self.x - 1][self.y + 1])
        if self.x < (self.w - 1) and self.y > 0:
            ac.append(self._map[self.x + 1][self.y - 1])
        if self.x < (self.w - 1) and self.y < (self.h - 1):
            ac.append(self._map[self.x + 1][self.y + 1])
        return ac

    def adjacent_nodes_hv(self):
        """returns horizontal and vertical adjacent coordinates"""
        ac = []
        if self.x > 0:
            ac.append(self._map[self.x - 1][self.y])
        if self.x < (self.w - 1):
            ac.append(self._map[self.x + 1][self.y])
        if self.y > 0:
            ac.append(self._map[self.x][self.y - 1])
        if self.y < (self.h - 1):
            ac.append(self._map[self.x][self.y + 1])
        return ac
