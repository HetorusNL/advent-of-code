class Queue:
    def __init__(self, size: int):
        self._queue: list[str] = []
        self._size: int = size
        self._chars_pushed = 0

    def push_back(self, char: str):
        self._queue.append(char)
        self._chars_pushed += 1
        while len(self._queue) > self._size:
            self._queue.pop(0)

    def header_found(self) -> bool:
        return len(set(self._queue)) == self._size

    def header_offset(self) -> int:
        return self._chars_pushed
