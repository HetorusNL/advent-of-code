class Tree:
    def __init__(self, height: int):
        self._height: int = height
        self._visible: bool = False

    @property
    def height(self):
        return self._height

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, _visible: bool):
        self._visible = _visible
