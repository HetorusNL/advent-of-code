class SNAFU:
    SNAFU_LUT = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}

    def __init__(self):
        pass

    @classmethod
    def from_snafu(cls, line: str) -> int:
        snafu_sum = 0
        for idx, char in enumerate(reversed(line)):
            snafu_sum += 5**idx * cls.SNAFU_LUT[char]
        return snafu_sum

    @classmethod
    def to_snafu(cls, number: int) -> str:
        # find the num of digits the snafu number will have
        num_digits = 1
        while 5 ** (num_digits - 1) * 2 < number:
            num_digits += 1

        # go from largest to smalles [num_digits, 1] and calculate snafu number
        snafu_number = ""
        for digit in range(num_digits - 1, -1, -1):
            partial_snafu = cls._from_partial_snafu(snafu_number, num_digits)
            num_2 = 5**digit * 2
            num_1 = 5**digit * 1
            num_0 = 5**digit * 0
            num_min_1 = 5**digit * -1
            num_min_2 = 5**digit * -2
            half_value = 5**digit * 0.5

            # check if the number is within half_value of the num checked
            if num_2 + partial_snafu + half_value > number and num_2 + partial_snafu - half_value < number:
                snafu_number += "2"
            elif num_1 + partial_snafu + half_value > number and num_1 + partial_snafu - half_value < number:
                snafu_number += "1"
            elif num_0 + partial_snafu + half_value > number and num_0 + partial_snafu - half_value < number:
                snafu_number += "0"
            elif num_min_1 + partial_snafu + half_value > number and num_min_1 + partial_snafu - half_value < number:
                snafu_number += "-"
            elif num_min_2 + partial_snafu + half_value > number and num_min_2 + partial_snafu - half_value < number:
                snafu_number += "="
        return snafu_number

    @classmethod
    def _from_partial_snafu(cls, partial_snafu: str, size: int) -> int:
        snafu = partial_snafu + "0" * (size - len(partial_snafu))
        return cls.from_snafu(snafu)
