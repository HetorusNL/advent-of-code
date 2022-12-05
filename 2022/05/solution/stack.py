class Stack:
    def __init__(self):
        self._stack: dict[str, list[str]] = {}

    def num_stacks(self) -> int:
        return len(self._stack.keys())

    def reverse_stack(self) -> None:
        for key in self._stack.keys():
            self._stack[key] = list(reversed(self._stack[key]))

    def push_back(self, idx: str, value: str) -> None:
        if idx not in self._stack.keys():
            self._stack[idx] = [value]
        else:
            self._stack[idx].append(value)

    def pop(self, idx: str) -> str:
        assert self._stack[idx], f"empty stack at {idx}!"
        return self._stack[idx].pop()

    def push_back_multiple(self, idx: str, values: list[str]) -> None:
        for value in values:
            self.push_back(idx, value)

    def pop_multiple(self, idx: str, num: int) -> list[str]:
        result = []
        for _ in range(num):
            result.append(self.pop(idx))
        return list(reversed(result))
