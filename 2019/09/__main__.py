import asyncio


class Mode(object):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    modes = {
        "0": POSITION,
        "1": IMMEDIATE,
        "2": RELATIVE,
    }


class Instruction(object):
    def __init__(self, computer, opcode):
        self.operations = {
            "01": computer.add,
            "02": computer.mul,
            "03": computer.inp,
            "04": computer.otp,
            "05": computer.jmpt,
            "06": computer.jmpf,
            "07": computer.lt,
            "08": computer.eq,
            "09": computer.arb,
            "99": computer.term,
        }

        opcode = opcode.zfill(5)
        # print(opcode)  # uncomment this for opcode debug purposes
        self.operation = self.operations[opcode[3:5]]
        self.param1_mode = Mode.modes[opcode[2]]
        self.param2_mode = Mode.modes[opcode[1]]
        self.param3_mode = Mode.modes[opcode[0]]


class ComputerIO(object):
    def __init__(self):
        # the ComputerIO object of the 'next' cpu
        self.output_computer_io = None
        # the list of input values, supplied by default and by 'previous' cpu
        self.input_values = []
        # the (copy of the) output values ofo this cpu
        self.output_values = []

    async def get_input(self, *args, **kwargs):
        while True:
            # print(f"returning from {self.input_values}")
            # wait until input values are present (provided by previous cpu)
            if len(self.input_values) == 0:
                # print("sleep")
                await asyncio.sleep(0)
                continue
            # print(f"outputting value: {self.input_values[0]}")
            input_value, *self.input_values = self.input_values
            return input_value

    def set_output(self, output_value):
        if self.output_computer_io is not None:
            # set the output as input of next cpu, if next cpu present
            self.output_computer_io.input_values.append(output_value)

        # also store a copy in output_values
        self.output_values.append(output_value)


class Computer(object):
    def __init__(self):
        self.IP = 0
        self.computer_io = ComputerIO()
        self.term_program = False
        self.relative_base = 0

    async def run(self, program):
        self.IP = 0  # reset the instruction pointer
        self.program = program  # store the program in the class
        self.term_program = False
        self.relative_base = 0
        while True:
            # run the instruction at the current IP position
            instruction = Instruction(self, str(self.ld_addr(self.IP)))
            await instruction.operation(instruction)
            if self.term_program:
                break

    # execute IP+3 = IP+1 + IP+2
    async def add(self, ins):
        self.st(
            self.IP + 3,
            self.ld(self.IP + 1, ins.param1_mode)
            + self.ld(self.IP + 2, ins.param2_mode),
            ins.param3_mode,
        )
        self.IP += 4

    # execute IP+3 = IP+1 * IP+2
    async def mul(self, ins):
        self.st(
            self.IP + 3,
            self.ld(self.IP + 1, ins.param1_mode)
            * self.ld(self.IP + 2, ins.param2_mode),
            ins.param3_mode,
        )
        self.IP += 4

    # terminate
    async def term(self, ins):
        # terminate by setting term_program to True
        self.term_program = True

    # input instruction, st_addr(IP+1, input())
    async def inp(self, ins):
        ip = await self.computer_io.get_input(">>> ")
        ip = int(ip)
        # the address where it's stored, should be fetched positional
        self.st(self.ld(self.IP + 1, Mode.POSITION), ip, ins.param1_mode)
        self.IP += 2

    # output instruction, print(ld_addr(addr))
    async def otp(self, ins):
        self.computer_io.set_output(self.ld(self.IP + 1, ins.param1_mode))
        self.IP += 2

    # jump-if-true
    async def jmpt(self, ins):
        if self.ld(self.IP + 1, ins.param1_mode):
            self.IP = self.ld(self.IP + 2, ins.param2_mode)
        else:  # false => no jump
            self.IP += 3

    # jump-if-false
    async def jmpf(self, ins):
        if not self.ld(self.IP + 1, ins.param1_mode):
            self.IP = self.ld(self.IP + 2, ins.param2_mode)
        else:  # true => no jump
            self.IP += 3

    # less than, execute IP+3 = IP+1 < IP+2 ? 1 : 0
    async def lt(self, ins):
        self.st(
            self.IP + 3,
            1
            if self.ld(self.IP + 1, ins.param1_mode)
            < self.ld(self.IP + 2, ins.param2_mode)
            else 0,
            ins.param3_mode,
        )
        self.IP += 4

    # equals, execute IP+3 = IP+1 == IP+2 ? 1 : 0
    async def eq(self, ins):
        self.st(
            self.IP + 3,
            1
            if self.ld(self.IP + 1, ins.param1_mode)
            == self.ld(self.IP + 2, ins.param2_mode)
            else 0,
            ins.param3_mode,
        )
        self.IP += 4

    # adjust the relative base by IP+1
    async def arb(self, ins):
        self.relative_base += self.ld(self.IP + 1, ins.param1_mode)
        self.IP += 2

    # load the value of the address where addr points to
    def ld(self, addr, mode):
        if mode == Mode.POSITION:
            return self.ld_addr(self.program.get(addr, 0))
        elif mode == Mode.IMMEDIATE:
            return self.ld_addr(addr)
        elif mode == Mode.RELATIVE:
            return self.ld_addr(self.relative_base + self.program.get(addr, 0))
        else:
            raise Exception(f"Invalid mode: {mode}!")

    # load the value of addr
    def ld_addr(self, addr):
        return self.program.get(addr, 0)

    # store the val in the address where addr points to
    def st(self, addr, val, mode):
        if mode == Mode.POSITION:
            self.st_addr(self.program.get(addr, 0), val)
        elif mode == Mode.IMMEDIATE:
            self.st_addr(addr, val)
        elif mode == Mode.RELATIVE:
            self.st_addr(self.relative_base + self.program.get(addr, 0), val)
        else:
            raise Exception(f"Invalid mode: {mode}!")

    # store the value in addr
    def st_addr(self, addr, val):
        self.program[addr] = val

    # return the value itself
    def val(self, val):
        return val


def part_1(program):
    computer = Computer()
    computer.computer_io.input_values.append(1)
    asyncio.get_event_loop().run_until_complete(computer.run(program.copy()))
    print("part_1 BOOST keycode:")
    print(computer.computer_io.output_values[0])


def part_2(program):
    computer = Computer()
    computer.computer_io.input_values.append(2)
    asyncio.get_event_loop().run_until_complete(computer.run(program.copy()))
    print("part_2 distress signal coordinates:")
    print(computer.computer_io.output_values[0])


if __name__ == "__main__":
    with open("input.txt") as f:
        program = dict(enumerate(map(int, f.readline().split(","))))

        part_1(program)

        part_2(program)
