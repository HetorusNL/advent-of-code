class Solution:
    def __init__(self):
        with open("input.txt") as f:
            self._lines = [l.strip() for l in f.readlines()]
        self._chars = {"(": ")", "[": "]", "{": "}", "<": ">"}
        self._illegal_char_points = {")": 3, "]": 57, "}": 1197, ">": 25137}
        self._completion_char_points = {")": 1, "]": 2, "}": 3, ">": 4}

    def solve(self):
        self.part_1()
        self.part_2()

    def part_1(self):
        illegal_chars = []
        for line in self._lines:
            _, illegal_char = self._process_line(line)
            if illegal_char:
                illegal_chars.append(illegal_char)
        score = sum(self._illegal_char_points[c] for c in illegal_chars)
        print(f"total syntax error score for these errors: {score}")

    def part_2(self):
        scores = []
        for line in self._lines:
            char_stack, illegal_char = self._process_line(line)
            if illegal_char:
                continue
            score = 0
            for char in reversed(char_stack):
                score *= 5
                score += self._completion_char_points[self._chars[char]]
            scores.append(score)
        scores.sort()
        print(f"incomplete line middle score: {scores[len(scores) // 2]}")

    def _process_line(self, line):
        char_stack = []
        illegal_chars = None
        for char in line:
            # handle illegal closing char with zero length stack
            if len(char_stack) == 0 and char in self._chars.values():
                illegal_chars = char
                break
            # handle length zero
            if len(char_stack) == 0:
                char_stack.append(char)
                continue
            # all opening chars can be added
            if char in self._chars.keys():
                char_stack.append(char)
                continue
            # match closing chars
            if char == self._chars[char_stack[-1]]:
                char_stack.pop()
                continue
            # if we end up here it's a syntax error
            # add the offending char and break
            illegal_chars = char
            break
        return char_stack, illegal_chars


if __name__ == "__main__":
    Solution().solve()
