import re

from solution.rope_part import RopePart


class Playfield:
    def __init__(self, snake_length: int):
        self._snake: list[RopePart] = [RopePart() for _ in range(snake_length)]
        self._snake_length = snake_length
        self._head: RopePart = self._snake[0]
        self._tail: RopePart = self._snake[self._snake_length - 1]
        self._tail_positions_visited: dict[str, int] = {self._tail.position: 1}

    def simulate(self, lines: list[str]) -> None:
        for line in lines:
            match = re.match(r"^(?P<direction>[LRUD])\s*(?P<num_steps>[0-9]*)$", line)
            assert match, f"invalid input provided {line}!"

            for _ in range(int(match["num_steps"])):
                self._update_head(match["direction"])
                for i in range(self._snake_length - 1):
                    self._update_tail(self._snake[i], self._snake[i + 1])
                self._tail_positions_visited[self._tail.position] = 1

    def get_num_visited_tail_positions(self) -> int:
        return len(self._tail_positions_visited)

    def _update_head(self, direction: str) -> None:
        match direction:
            case "U":
                self._head.y += 1
            case "D":
                self._head.y -= 1
            case "L":
                self._head.x -= 1
            case "R":
                self._head.x += 1

    def _update_tail(self, part1: RopePart, part2: RopePart) -> None:
        dx: int = abs(part1.x - part2.x)
        dy: int = abs(part1.y - part2.y)
        # handle the do nothing case
        if dx <= 1 and dy <= 1:
            return
        # handle the case where dy == 0
        if dy == 0:
            if part1.x - part2.x > 0:
                part2.x += 1
            elif part1.x - part2.x < 0:
                part2.x -= 1
            return
        # handle the case where dx == 0
        if dx == 0:
            if part1.y - part2.y > 0:
                part2.y += 1
            elif part1.y - part2.y < 0:
                part2.y -= 1
            return
        # otherwise perform a diagonal move
        if part1.x - part2.x > 0:
            part2.x += 1
        elif part1.x - part2.x < 0:
            part2.x -= 1
        if part1.y - part2.y > 0:
            part2.y += 1
        elif part1.y - part2.y < 0:
            part2.y -= 1
        return
