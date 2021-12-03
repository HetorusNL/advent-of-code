import asyncio


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
            "99": computer.term,
        }

        opcode = opcode.zfill(5)
        # print(opcode)  # uncomment this for opcode debug purposes
        self.operation = self.operations[opcode[3:5]]
        self.param1 = opcode[2] != "0"
        self.param2 = opcode[1] != "0"
        self.param3 = opcode[0] != "0"


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

    async def run(self, program):
        self.IP = 0  # reset the instruction pointer
        self.program = program  # store the program in the class
        while self.IP < len(self.program):
            # run the instruction at the current IP position
            instruction = Instruction(self, str(self.ld_addr(self.IP)))
            await instruction.operation(instruction)

    # execute IP+3 = IP+1 + IP+2
    async def add(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        param3 = self.st_addr if ins.param3 else self.st
        param3(self.IP + 3, param1(self.IP + 1) + param2(self.IP + 2))
        self.IP += 4

    # execute IP+3 = IP+1 * IP+2
    async def mul(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        param3 = self.st_addr if ins.param3 else self.st
        param3(self.IP + 3, param1(self.IP + 1) * param2(self.IP + 2))
        self.IP += 4

    # terminate
    async def term(self, ins):
        # terminate by setting the IP to the size of the program
        self.IP = len(self.program)

    # input instruction, st_addr(IP+1, input())
    async def inp(self, ins):
        ip = await self.computer_io.get_input(">>> ")
        ip = int(ip)
        self.st_addr(
            self.ld_addr(self.IP + 1), ip,
        )
        self.IP += 2

    # output instruction, print(ld_addr(addr))
    async def otp(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        self.computer_io.set_output(param1(self.IP + 1))
        self.IP += 2

    # jump-if-true
    async def jmpt(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        if param1(self.IP + 1):
            self.IP = param2(self.IP + 2)
        else:  # false => no jump
            self.IP += 3

    # jump-if-false
    async def jmpf(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        if not param1(self.IP + 1):
            self.IP = param2(self.IP + 2)
        else:  # true => no jump
            self.IP += 3

    # less than, execute IP+3 = IP+1 < IP+2 ? 1 : 0
    async def lt(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        param3 = self.st_addr if ins.param3 else self.st
        param3(
            self.IP + 3, 1 if param1(self.IP + 1) < param2(self.IP + 2) else 0
        )
        self.IP += 4

    # equals, execute IP+3 = IP+1 == IP+2 ? 1 : 0
    async def eq(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        param3 = self.st_addr if ins.param3 else self.st
        param3(
            self.IP + 3, 1 if param1(self.IP + 1) == param2(self.IP + 2) else 0
        )
        self.IP += 4

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

    # return the value itself
    def val(self, val):
        return val


def run_on_amplifiers(program, phase, loopback):
    # generate 5 computers with the phase supplied as input
    computers = []
    for i in range(5):
        computer = Computer()
        computer.computer_io.input_values.append(phase[i])
        computers.append(computer)

    # chain the computers one after each other
    computers[0].computer_io.output_computer_io = computers[1].computer_io
    computers[1].computer_io.output_computer_io = computers[2].computer_io
    computers[2].computer_io.output_computer_io = computers[3].computer_io
    computers[3].computer_io.output_computer_io = computers[4].computer_io
    # if loopback is enabled, chain computer 4 to computer 0
    if loopback:
        computers[4].computer_io.output_computer_io = computers[0].computer_io

    # bootstrap the first computer with value 0
    computers[0].computer_io.input_values.append(0)

    # run all computers concurrently until they all have called term(ins)
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            *[computer.run(program.copy()) for computer in computers]
        )
    )

    # return the last output value of the last computer
    return computers[4].computer_io.output_values[-1]


def permutation(input_list):
    if len(input_list) == 0:
        return []  # empty, no permutations

    if len(input_list) == 1:
        return [input_list]  # only 1 permutation possible

    current_permutations = []  # store the current permutations

    for index, value in enumerate(input_list):

        remaining_list = input_list[:index] + input_list[index + 1 :]

        # generate all permutations with value as first element
        for p in permutation(remaining_list):
            current_permutations.append([value] + p)

    return current_permutations


def part_1(program):
    # make a copy so we don't alter the original program
    part_1_program = program.copy()

    # run the program on the amplifiers
    print("beginning part_1 program:")
    thrust_values = []
    for perm in permutation([0, 1, 2, 3, 4]):
        thrust_values.append(run_on_amplifiers(part_1_program, perm, False))

    print("end of part_1 program")
    print(f"max thrust: {max(thrust_values)}")


def part_2(program):
    # make a copy so we don't alter the original program
    part_2_program = program.copy()

    # run the program on the amplifiers
    print("beginning part_2 program:")
    thrust_values = []
    for perm in permutation([5, 6, 7, 8, 9]):
        thrust_values.append(run_on_amplifiers(part_2_program, perm, True))

    print("end of part_2 program")
    print(f"max thrust: {max(thrust_values)}")


if __name__ == "__main__":
    with open("input.txt") as f:
        program = list(map(int, f.readline().split(",")))

        part_1(program)

        part_2(program)

