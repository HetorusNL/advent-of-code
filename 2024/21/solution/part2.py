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


class MoveState:
    move_state_cache: dict[str, list["MoveState"]] = {}
    numeric_keypad: dict[str, Pos] = {
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
    directional_keypad: dict[str, Pos] = {
        "<": Pos(0, 0),
        "v": Pos(1, 0),
        ">": Pos(2, 0),
        "^": Pos(1, 1),
        "A": Pos(2, 1),
    }

    def __init__(self, sequence: str, amount: int):
        self.sequence = sequence
        self.amount = amount

    def next_robot_move_state(self) -> list["MoveState"]:
        if self.sequence not in self.move_state_cache:
            self._calculate_sequence()
        resulting_states: list[MoveState] = []
        for move_state in self.move_state_cache[self.sequence]:
            resulting_states.append(MoveState(move_state.sequence, self.amount * move_state.amount))
        return resulting_states

    def _single_step_single(self, state: State, end_pos: Pos, keypad_values: list[Pos]) -> list[State]:
        states: list[State] = []
        if state.pos == end_pos:
            # we have moved, press the "A" button
            states.append(State(state.command + "A", state.pos))
        # try every direction, for some reason this order (<, ^, v, >) is the cheapest..
        if state.pos.x > end_pos.x:
            new_pos: Pos = Pos(state.pos.x - 1, state.pos.y)
            if new_pos in keypad_values:
                states.extend(self._single_step_single(State(state.command + "<", new_pos), end_pos, keypad_values))
        if state.pos.y < end_pos.y:
            new_pos: Pos = Pos(state.pos.x, state.pos.y + 1)
            if new_pos in keypad_values:
                states.extend(self._single_step_single(State(state.command + "^", new_pos), end_pos, keypad_values))
        if state.pos.y > end_pos.y:
            new_pos: Pos = Pos(state.pos.x, state.pos.y - 1)
            if new_pos in keypad_values:
                states.extend(self._single_step_single(State(state.command + "v", new_pos), end_pos, keypad_values))
        if state.pos.x < end_pos.x:
            new_pos: Pos = Pos(state.pos.x + 1, state.pos.y)
            if new_pos in keypad_values:
                states.extend(self._single_step_single(State(state.command + ">", new_pos), end_pos, keypad_values))
        return states

    def _single_step(self, states: list[State], end_pos: Pos, keypad_values: list[Pos]):
        finished_states: list[State] = []
        for state in states:
            finished_states.extend(self._single_step_single(state, end_pos, keypad_values))
        return finished_states

    def _calculate_sequence(self):
        move_states: list[MoveState] = []
        # calculate the minimum amount of steps, starting at "A"
        states: list[State] = [State("", self.directional_keypad["A"])]
        # plan the sequence from "A" to our sequence itself and end at "A" again
        for value in self.sequence + "A":
            end_pos: Pos = self.directional_keypad[value]
            states = self._single_step(states, end_pos, list(self.directional_keypad.values()))
        # calculate the weight of the states by tracing the distance
        # start from "A", do the whole sequence, and end at "A" again
        weights: dict[int, list[State]] = {}
        for state in states:
            distance: int = 0
            first: str = "A"
            for char in state.command:
                pos_from: Pos = self.directional_keypad[first]
                pos_to: Pos = self.directional_keypad[char]
                distance += abs(pos_from.x - pos_to.x) + abs(pos_from.y - pos_to.y)
                first = char
            if distance not in weights:
                weights[distance] = []
            weights[distance].append(state)
        # get the first state that has the lowest weight (because of single_step order)
        state = weights[min(weights.keys())][0]
        moves: dict[str, int] = {}
        move: str = ""
        for char in state.command:
            if char == "A":
                if move not in moves:
                    moves[move] = 0
                moves[move] += 1
                move = ""
            else:
                move += char
        for sequence, amount in moves.items():
            move_states.append(MoveState(sequence, amount))
        # store in the cache
        self.move_state_cache[self.sequence] = move_states

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'<"{self.sequence}", {self.amount}>'


class Part2:
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

    def keypad_press_single(self, state: State, end_pos: Pos, keypad_values: list[Pos]) -> list[State]:
        states: list[State] = []
        if state.pos == end_pos:
            # we have moved, press the "A" button
            states.append(State(state.command + "A", state.pos))
        if state.pos.x < end_pos.x:
            new_pos: Pos = Pos(state.pos.x + 1, state.pos.y)
            if new_pos in keypad_values:
                states.extend(self.keypad_press_single(State(state.command + ">", new_pos), end_pos, keypad_values))
        if state.pos.x > end_pos.x:
            new_pos: Pos = Pos(state.pos.x - 1, state.pos.y)
            if new_pos in keypad_values:
                states.extend(self.keypad_press_single(State(state.command + "<", new_pos), end_pos, keypad_values))
        if state.pos.y < end_pos.y:
            new_pos: Pos = Pos(state.pos.x, state.pos.y + 1)
            if new_pos in keypad_values:
                states.extend(self.keypad_press_single(State(state.command + "^", new_pos), end_pos, keypad_values))
        if state.pos.y > end_pos.y:
            new_pos: Pos = Pos(state.pos.x, state.pos.y - 1)
            if new_pos in keypad_values:
                states.extend(self.keypad_press_single(State(state.command + "v", new_pos), end_pos, keypad_values))
        return states

    def keypad_press(self, states: list[State], end_pos: Pos, keypad_values: list[Pos]):
        finished_states: list[State] = []
        for state in states:
            finished_states.extend(self.keypad_press_single(state, end_pos, keypad_values))
        return finished_states

    def first_keypad(self, code: str) -> list[State]:
        states: list[State] = [State("", self.numeric_keypad["A"])]
        for value in code:
            end_pos: Pos = self.numeric_keypad[value]
            states = self.keypad_press(states, end_pos, list(self.numeric_keypad.values()))
        return states

    def solve(self) -> None:
        print("solving...")
        self.generate_keypads()
        self.result = 0
        for line in self.lines:
            # run 1 robot with a numerical keypad
            states = self.first_keypad(line)
            results: list[int] = []
            length: int = 0
            # perform the algorithm for all states we got from the first keypad
            for state in states:
                # split the moves into separate objects
                move_states: dict[str, MoveState] = {}
                moves: dict[str, int] = {}
                move: str = ""
                for char in state.command:
                    if char == "A":
                        if move not in moves:
                            moves[move] = 0
                        moves[move] += 1
                        move = ""
                    else:
                        move += char
                for sequence, amount in moves.items():
                    if sequence in move_states:
                        move_states[sequence].amount += amount
                    else:
                        move_states[sequence] = MoveState(sequence, amount)
                length: int = 0
                # run 25 robots with a directional keypad
                for _ in range(25):
                    length = 0
                    next_move_states: dict[str, MoveState] = {}
                    for move_state in move_states.values():
                        for next_move_state in move_state.next_robot_move_state():
                            # add the length of the sequence and the trailing "A"
                            length += next_move_state.amount * (1 + len(next_move_state.sequence))
                            if next_move_state.sequence in next_move_states:
                                next_move_states[next_move_state.sequence].amount += next_move_state.amount
                            else:
                                next_move_states[next_move_state.sequence] = MoveState(
                                    next_move_state.sequence, next_move_state.amount
                                )
                    move_states = next_move_states
                results.append(length)
            number = int(line[:3])
            self.result += min(results) * number

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
