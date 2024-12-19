from pathlib import Path


class State:
    def __init__(self, index: int, pattern: str):
        self.index = index
        self.pattern = pattern
        # if we point after the pattern length, we're done
        self.completed = self.index == len(pattern)

    def fits(self, towel: str) -> bool:
        # make sure the towel length fully fits
        if len(self.pattern) - self.index < len(towel):
            return False
        # check that the pattern matches
        return self.pattern[self.index : self.index + len(towel)] == towel

    def add(self, towel: str) -> "State":
        return State(self.index + len(towel), self.pattern)

    def __eq__(self, other: object) -> bool:
        assert type(other) == State
        return self.index == other.index and self.pattern == other.pattern

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"<index: {self.index}, pattern: {self.pattern}, completed: {self.completed}]"

    def __hash__(self) -> int:
        return hash(str(self))


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def cycle_single(self, state: State) -> list[State]:
        new_states: list[State] = []
        # add all possible matches of a towel for this state
        for towel in self.towels:
            if state.fits(towel):
                new_states.append(state.add(towel))
        return new_states

    def cycle(self, states: list[State]) -> list[State]:
        new_states: list[State] = []
        # add all matches for this list of states
        for state in states:
            new_states.extend(self.cycle_single(state))
        # remove duplicates
        new_states = list(set(new_states))

        # when any state is completed, or we ran out of possibilities, return
        if any(state.completed for state in new_states) or not new_states:
            return new_states
        else:
            # otherwise recursively continue
            return self.cycle(new_states)

    def solve(self) -> None:
        print("solving...")
        self.result: int = 0
        self.towels: list[str] = [towel.strip() for towel in self.lines[0].split(",")]
        self.patterns: list[str] = [pattern.strip() for pattern in self.lines[2:]]
        for pattern in self.patterns:
            state = State(0, pattern)
            if any(s.completed for s in self.cycle([state])):
                self.result += 1

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
