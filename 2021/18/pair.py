class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.parent = None
        if isinstance(self.left, Pair):
            self.left._set_parent(self)
        if isinstance(self.right, Pair):
            self.right._set_parent(self)

    def __eq__(self, other):
        if isinstance(other, Pair):
            return id(self) == id(other)
        return False

    def _set_parent(self, parent):
        self.parent = parent

    def get_depth(self, depth=1):
        if self.parent:
            return self.parent.get_depth(depth + 1)
        return depth

    def get_string(self):
        left = (
            self.left.get_string()
            if isinstance(self.left, Pair)
            else self.left
        )
        right = (
            self.right.get_string()
            if isinstance(self.right, Pair)
            else self.right
        )
        return f"[{left},{right}]"

    def reduce(self):
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break
        return self

    def explode(self):
        if self.get_depth() > 4:
            if self == self.parent.left:
                if isinstance(self.parent.right, Pair):
                    self.parent.right._add_up_to_left(self.right)
                else:
                    self.parent.right += self.right
            else:
                self.parent._add_down_to_right(self.right)
            if self == self.parent.right:
                if isinstance(self.parent.left, Pair):
                    self.parent.left._add_up_to_right(self.left)
                else:
                    self.parent.left += self.left
            else:
                self.parent._add_down_to_left(self.left)
            if self == self.parent.left:
                self.parent.left = 0
            if self == self.parent.right:
                self.parent.right = 0
            return True
        if isinstance(self.left, Pair):
            if self.left.explode():
                return True
        if isinstance(self.right, Pair):
            if self.right.explode():
                return True
        return False

    def split(self):
        if isinstance(self.left, Pair):
            if self.left.split():
                return True
        else:
            if self.left >= 10:
                left = self.left // 2
                right = self.left - left
                self.left = Pair(left, right)
                self.left._set_parent(self)
                return True
        if isinstance(self.right, Pair):
            if self.right.split():
                return True
        else:
            if self.right >= 10:
                left = self.right // 2
                right = self.right - left
                self.right = Pair(left, right)
                self.right._set_parent(self)
                return True

    def _add_down_to_right(self, value):
        if not isinstance(self.right, Pair):
            self.right += value
            return
        if not self.parent:
            return
        if self == self.parent.left:
            if isinstance(self.parent.right, Pair):
                self.parent.right._add_up_to_left(value)
            else:
                self.parent.right += value
        else:
            self.parent._add_down_to_right(value)

    def _add_up_to_left(self, value):
        if not isinstance(self.left, Pair):
            self.left += value
            return
        self.left._add_up_to_left(value)

    def _add_down_to_left(self, value):
        if not isinstance(self.left, Pair):
            self.left += value
            return
        if not self.parent:
            return
        if self == self.parent.right:
            if isinstance(self.parent.left, Pair):
                self.parent.left._add_up_to_right(value)
            else:
                self.parent.left += value
        else:
            self.parent._add_down_to_left(value)

    def _add_up_to_right(self, value):
        if not isinstance(self.right, Pair):
            self.right += value
            return
        self.right._add_up_to_right(value)

    def get_magnitude(self):
        magnitude = 0
        if isinstance(self.left, Pair):
            magnitude += 3 * self.left.get_magnitude()
        else:
            magnitude += 3 * self.left
        if isinstance(self.right, Pair):
            magnitude += 2 * self.right.get_magnitude()
        else:
            magnitude += 2 * self.right
        return magnitude
