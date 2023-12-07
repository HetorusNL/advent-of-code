class Hand1:
    def __init__(self, cards: str, bid: str):
        self.score = "23456789TJQKA"

        self.cards = cards
        self.bid = int(bid)
        self.hand: dict[str, int] = {}
        for card in cards:
            if card not in self.hand:
                self.hand[card] = 1
            else:
                self.hand[card] += 1

    def __lt__(self, other: "Hand1") -> bool:
        self_hand = list(self.hand.values())
        other_hand = list(other.hand.values())
        max_self_hand = max(self_hand)
        max_other_hand = max(other_hand)
        if max_self_hand != 5 and max_other_hand == 5:
            return True
        elif max_self_hand == 5 and max_other_hand != 5:
            return False
        elif max_self_hand == 5 and max_other_hand == 5:
            return self.has_lower_card(other)
        elif max_self_hand != 4 and max_other_hand == 4:
            return True
        elif max_self_hand == 4 and max_other_hand != 4:
            return False
        elif max_self_hand == 4 and max_other_hand == 4:
            return self.has_lower_card(other)
        elif (3 not in self_hand or 2 not in self_hand) and (3 in other_hand and 2 in other_hand):
            return True
        elif (3 in self_hand and 2 in self_hand) and (3 not in other_hand or 2 not in other_hand):
            return False
        elif 3 in self_hand and 2 in self_hand and 3 in other_hand and 2 in other_hand:
            return self.has_lower_card(other)
        elif max_self_hand != 3 and max_other_hand == 3:
            return True
        elif max_self_hand == 3 and max_other_hand != 3:
            return False
        elif max_self_hand == 3 and max_other_hand == 3:
            return self.has_lower_card(other)
        elif self_hand.count(2) != 2 and other_hand.count(2) == 2:
            return True
        elif self_hand.count(2) == 2 and other_hand.count(2) != 2:
            return False
        elif self_hand.count(2) == 2 and other_hand.count(2) == 2:
            return self.has_lower_card(other)
        elif max_self_hand != 2 and max_other_hand == 2:
            return True
        elif max_self_hand == 2 and max_other_hand != 2:
            return False
        elif max_self_hand == 2 and max_other_hand == 2:
            return self.has_lower_card(other)
        elif len(self_hand) == 5 and len(other_hand) == 5:
            for score in self.score:
                if score not in self_hand and score in other_hand:
                    return True
                elif score in self_hand and score not in other_hand:
                    return False

        return self.has_lower_card(other)

    def has_lower_card(self, other: "Hand1") -> bool:
        for card_idx in range(len(self.cards)):
            if self.score.index(self.cards[card_idx]) != self.score.index(other.cards[card_idx]):
                result = self.score.index(self.cards[card_idx]) < self.score.index(other.cards[card_idx])
                return result
        assert False
