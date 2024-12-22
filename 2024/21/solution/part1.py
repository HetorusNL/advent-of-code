from pathlib import Path


class Pos:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __eq__(self, other: object) -> bool:
        assert type(other) == Pos
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    def __hash__(self) -> int:
        return hash(str(self))


class State:
    def __init__(self, command: str, pos: Pos):
        self.command: str = command
        self.pos: Pos = pos

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'<"{self.command}", {self.pos}>'

    def __hash__(self) -> int:
        return hash(str(self))


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def generate_keypads(self):
        self.numeric_keypad: dict[str, Pos] = {
            "0": Pos(1, 0),
            "A": Pos(2, 0),
            "1": Pos(0, 1),
            "2": Pos(1, 1),
            "3": Pos(2, 1),
            "4": Pos(0, 2),
            "5": Pos(1, 2),
            "6": Pos(2, 2),
            "7": Pos(0, 3),
            "8": Pos(1, 3),
            "9": Pos(2, 3),
        }
        self.directional_keypad: dict[str, Pos] = {
            "<": Pos(0, 0),
            "v": Pos(1, 0),
            ">": Pos(2, 0),
            "^": Pos(1, 1),
            "A": Pos(2, 1),
        }

    def keypad_press(self, states: list[State], end_pos: Pos, keypad_values: list[Pos]):
        finished_states: list[State] = []
        while states:
            new_states: list[State] = []
            for state in states:
                if state.pos == end_pos:
                    # we have moved, press the "A" button
                    finished_states.append(State(state.command + "A", state.pos))
                    continue
                # try every direction until we reach the end pos
                if state.pos.x < end_pos.x:
                    new_pos: Pos = Pos(state.pos.x + 1, state.pos.y)
                    if new_pos in keypad_values:
                        new_states.append(State(state.command + ">", new_pos))
                elif state.pos.x > end_pos.x:
                    new_pos: Pos = Pos(state.pos.x - 1, state.pos.y)
                    if new_pos in keypad_values:
                        new_states.append(State(state.command + "<", new_pos))
                if state.pos.y < end_pos.y:
                    new_pos: Pos = Pos(state.pos.x, state.pos.y + 1)
                    if new_pos in keypad_values:
                        new_states.append(State(state.command + "^", new_pos))
                elif state.pos.y > end_pos.y:
                    new_pos: Pos = Pos(state.pos.x, state.pos.y - 1)
                    if new_pos in keypad_values:
                        new_states.append(State(state.command + "v", new_pos))
            states = new_states
        return finished_states

    def first_keypad(self, code: str) -> list[State]:
        # from "A" go through all numbers on the numeric keypad
        states: list[State] = [State("", self.numeric_keypad["A"])]
        for value in code:
            end_pos: Pos = self.numeric_keypad[value]
            states = self.keypad_press(states, end_pos, list(self.numeric_keypad.values()))
        return states

    def second_keypad(self, old_states: list[State]) -> list[State]:
        # from "A" go through all the sequences resulting from the first keypad
        final_states: list[State] = []
        for old_state in old_states:
            states: list[State] = [State("", self.directional_keypad["A"])]
            for value in old_state.command:
                end_pos: Pos = self.directional_keypad[value]
                states = self.keypad_press(states, end_pos, list(self.directional_keypad.values()))
            final_states.extend(states)
        return final_states

    def final_keypad(self, old_states: list[State]) -> int:
        # small optimization of the final keypad to only get the lowest command length
        # still go from "A" through all the sequences resulting from the second keypad
        lowest_command_length: int | None = None
        for old_state in old_states:
            states: list[State] = [State("", self.directional_keypad["A"])]
            for value in old_state.command:
                end_pos: Pos = self.directional_keypad[value]
                states = self.keypad_press(states, end_pos, list(self.directional_keypad.values()))
            command_length = min(len(state.command) for state in states)
            if lowest_command_length is None:
                lowest_command_length = command_length
            lowest_command_length = min(lowest_command_length, command_length)
        assert lowest_command_length
        return lowest_command_length

    def solve(self) -> None:
        print("solving...")
        self.generate_keypads()
        self.result = 0
        for line in self.lines:
            states = self.first_keypad(line)
            states = self.second_keypad(states)
            shortest = min(len(state.command) for state in states)
            states = [state for state in states if len(state.command) == shortest]
            length = self.final_keypad(states)
            number = int(line[:3])
            self.result += length * number

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
