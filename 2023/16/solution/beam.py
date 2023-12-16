class Beam:
    def __init__(self, row: int, col: int, direction: str, lines: list[str]):
        self.row = row
        self.col = col
        self.direction = direction
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)
        self.char = lines[row][col]

    def get_next(self) -> list["Beam"]:
        match self.char:
            case ".":
                return self.exists([self.beam_to(self.direction)])
            case "\\":
                match self.direction:
                    case "r":
                        return self.exists([self.beam_to("d")])
                    case "d":
                        return self.exists([self.beam_to("r")])
                    case "l":
                        return self.exists([self.beam_to("u")])
                    case "u":
                        return self.exists([self.beam_to("l")])
            case "/":
                match self.direction:
                    case "r":
                        return self.exists([self.beam_to("u")])
                    case "d":
                        return self.exists([self.beam_to("l")])
                    case "l":
                        return self.exists([self.beam_to("d")])
                    case "u":
                        return self.exists([self.beam_to("r")])
            case "-":
                match self.direction:
                    case "r":
                        return self.exists([self.beam_to("r")])
                    case "d":
                        return self.exists([self.beam_to("l"), self.beam_to("r")])
                    case "l":
                        return self.exists([self.beam_to("l")])
                    case "u":
                        return self.exists([self.beam_to("l"), self.beam_to("r")])
            case "|":
                match self.direction:
                    case "r":
                        return self.exists([self.beam_to("u"), self.beam_to("d")])
                    case "d":
                        return self.exists([self.beam_to("d")])
                    case "l":
                        return self.exists([self.beam_to("u"), self.beam_to("d")])
                    case "u":
                        return self.exists([self.beam_to("u")])
        assert False

    def beam_to(self, direction: str) -> list:
        match direction:
            case "r":
                return [self.row, self.col + 1, direction]
            case "d":
                return [self.row + 1, self.col, direction]
            case "l":
                return [self.row, self.col - 1, direction]
            case "u":
                return [self.row - 1, self.col, direction]
        assert False

    def exists(self, beams_info: list[list]) -> list["Beam"]:
        valid_beams: list["Beam"] = []
        for beam_info in beams_info:
            row, col, direction = beam_info
            if col >= 0 and col < self.width:
                if row >= 0 and row < self.height:
                    valid_beams.append(Beam(row, col, direction, self.lines))
        return valid_beams
