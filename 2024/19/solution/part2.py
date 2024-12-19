from pathlib import Path


class State:
    def __init__(self, index: int, pattern: str, count: int):
        self.index = index
        self.pattern = pattern
        self.length = len(pattern)
        self.count = count
        # if we point after the pattern length, we're done
        self.completed = self.index == self.length
        # precompute the str and the hash
        self.string = self.__str__()
        self.state_hash = hash(self.string)

    def fits(self, towel: str, towel_length: int) -> bool:
        # make sure the towel length fully fits
        if self.length - self.index < towel_length:
            return False
        # check that the pattern matches
        return self.pattern[self.index : self.index + towel_length] == towel

    def add(self, towel_length: int) -> "State":
        return State(self.index + towel_length, self.pattern, self.count)

    def __eq__(self, other: object) -> bool:
        assert type(other) == State
        return self.index == other.index and self.pattern == other.pattern

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<{self.index}, {self.pattern}, {self.completed}, {self.count}]"

    def __hash__(self) -> int:
        return self.state_hash


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def cycle_single(self, state: State) -> dict[int, State]:
        # if already solved, return state as is
        if state.completed:
            return {state.state_hash: state}
        new_states: dict[int, State] = {}
        # add all possible matches of a towel for this state
        for towel, length in self.towels.items():
            if state.fits(towel, length):
                new_state = state.add(length)
                if new_state.state_hash in new_states:
                    new_states[new_state.state_hash].count += new_state.count
                else:
                    new_states[new_state.state_hash] = new_state
        return new_states

    def cycle(self, states: dict[int, dict[int, State]]) -> dict[int, dict[int, State]]:
        # add all matches for this list of states
        # start with the lowest index
        lowest_index = min(states.keys())
        for state in states[lowest_index].values():
            for new_state in self.cycle_single(state).values():
                if new_state.index not in states:
                    states[new_state.index] = {}
                # either add the count if a similar state exists, or create a new one
                if new_state.state_hash in states[new_state.index]:
                    states[new_state.index][new_state.state_hash].count += new_state.count
                else:
                    states[new_state.index][new_state.state_hash] = new_state
        # remove the processed items
        del states[lowest_index]
        # if we don't have any states left, return
        if not states:
            return states
        # every state is completed, or we ran out of possibilities, return
        if len(states.keys()) == 1 and all(state.completed for state in states[list(states.keys())[0]].values()):
            return states
        # otherwise recursively continue
        return self.cycle(states)

    def solve(self) -> None:
        print("solving...")
        self.result: int = 0
        self.towels: dict[str, int] = {towel.strip(): len(towel.strip()) for towel in self.lines[0].split(",")}
        self.patterns: list[str] = [pattern.strip() for pattern in self.lines[2:]]
        for pattern in self.patterns:
            state = State(0, pattern, 1)
            states = self.cycle({0: {state.state_hash: state}})
            if states:
                assert len(states.keys()) == 1
                self.result += sum(state.count for state in states[list(states.keys())[0]].values())

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
