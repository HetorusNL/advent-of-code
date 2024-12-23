from pathlib import Path


class Buyer:
    def __init__(self, initial_number: int):
        # first generate the price delta list
        secret: int = initial_number
        prices: list[int] = [self.get_price(secret)]
        changes: list[int] = []
        for _ in range(2000):
            secret = self.evolve_secret(secret)
            prices.append(self.get_price(secret))
            changes.append(prices[-1] - prices[-2])
        # remove the first element in the prices list to get 2000 elements
        prices.pop(0)
        # precalculate all sequences, and hash the sequence to int16
        self.sequence_cache: dict[int, int] = {}
        for i in range(len(changes) - 4):
            sequence: int = 0
            for j in range(4):
                sequence += changes[i + j] * (1 << j * 4)
            if sequence not in self.sequence_cache:
                self.sequence_cache[sequence] = prices[i + 3]

    def evolve_secret(self, previous: int) -> int:
        # step 1
        secret: int = ((previous * 64) ^ previous) % 16777216
        # step 2
        secret = ((secret // 32) ^ secret) % 16777216
        # step 3
        secret = ((secret * 2048) ^ secret) % 16777216
        # return the new secret
        return secret

    def get_price(self, secret: int) -> int:
        # get the price, the last digit of the secret number
        return int(str(secret)[-1])

    def bananas_for_sequence(self, sequence: int) -> int:
        return self.sequence_cache.get(sequence, 0)


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def process_sequence(self, sequence: int) -> int:
        # calculate the total number of bananas for all buyers for this sequence
        total_bananas: int = 0
        for buyer in self.buyers:
            total_bananas += buyer.bananas_for_sequence(sequence)
        return total_bananas

    def process_buyer(self, buyer: Buyer):
        for sequence in buyer.sequence_cache.keys():
            # if the sequence is already processed, skip it
            if sequence in self.bananas_sequence_cache:
                continue
            # otherwise process the sequence on all buyers
            bananas: int = self.process_sequence(sequence)
            self.bananas_sequence_cache[sequence] = bananas

    def solve(self) -> None:
        print("solving...")
        self.buyers: list[Buyer] = []
        # key: int hash of the sequence, value: number of bananas
        self.bananas_sequence_cache: dict[int, int] = {}
        # process the input and precalculate the buyers
        for line in self.lines:
            self.buyers.append(Buyer(int(line)))
        # loop through all buyers to get the changes sequence
        for buyer in self.buyers:
            print(buyer)
            self.process_buyer(buyer)
        self.result = max(self.bananas_sequence_cache.values())

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
