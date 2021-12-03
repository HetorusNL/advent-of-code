class Computer(object):
    def __init__(self):
        self.opcode = {"1": self.add, "2": self.mul, "99": self.term}
        self.IP = 0

    def run(self, program):
        self.IP = 0  # reset the instruction pointer
        self.program = program  # store the program in the class
        while self.IP < len(self.program):
            # run the instruction at the current IP position
            self.opcode[str(self.ld_addr(self.IP))]()

    # execute IP+3 = IP+1 + IP+2
    def add(self):
        self.st(self.IP + 3, self.ld(self.IP + 1) + self.ld(self.IP + 2))
        self.IP += 4

    # execute IP+3 = IP+1 * IP+2
    def mul(self):
        self.st(self.IP + 3, self.ld(self.IP + 1) * self.ld(self.IP + 2))
        self.IP += 4

    # terminate
    def term(self):
        # terminate by setting the IP to the size of the program
        self.IP = len(self.program)

    # load the value of the address where addr points to
    def ld(self, addr):
        return self.ld_addr(self.program[addr])

    # load the value of addr
    def ld_addr(self, addr):
        return self.program[addr]

    # store the val in the address where addr points to
    def st(self, addr, val):
        self.st_addr(self.program[addr], val)

    # store the value in addr
    def st_addr(self, addr, val):
        self.program[addr] = val


def part_1(program):
    computer = Computer()
    # make a copy so we don't alter the original program
    part_1_program = program.copy()

    # set the two values and run the program
    part_1_program[1] = 12
    part_1_program[2] = 2
    computer.run(part_1_program)

    print("value in register 0 for part_1:")
    print(computer.ld_addr(0))


def part_2(program):
    computer = Computer()
    # make a copy so we don't alter the original program
    part_2_program = program.copy()

    for noun in range(100):
        for verb in range(100):
            # make (again) a copy of the program, set the noun and verb and run
            part_2_program_copy = part_2_program.copy()
            part_2_program_copy[1] = noun
            part_2_program_copy[2] = verb
            computer.run(part_2_program_copy)
            if computer.ld_addr(0) == 19690720:
                print(
                    "(100 * noun + verb) value when register 0 is 19690720 "
                    "for part_2:"
                )
                print(100 * noun + verb)


if __name__ == "__main__":
    with open("input.txt") as f:
        program = list(map(int, f.readline().split(",")))
        part_1(program)

        part_2(program)
