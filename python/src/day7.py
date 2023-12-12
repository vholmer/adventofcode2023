from enum import Enum
from typing import List

TRANSLATE = {
    "A": "F",
    "K": "E",
    "Q": "D",
    "J": "C",
    "T": "B",
}

class HandType(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7

class Hand:
    cards: dict
    bid: int
    hand: str

    def __init__(self, hand, bid) -> None:
        self.cards = {}
        self.bid = bid
        self.hand = hand
    
        for card in hand:
            if card not in self.cards:
                self.cards[card] = 1
            else:
                self.cards[card] += 1

    def __str__(self) -> str:
        return self.hand

    def __repr__(self) -> str:
        return self.hand

    def hand_type(self) -> HandType:
        max_card = max(self.cards.values())

        if max_card < 5:
            second_max_card = sorted(self.cards.values(), reverse=True)[1]
        else:
            second_max_card = 0

        high_card = not any([x for x in self.cards.values() if x > 1])

        if max_card == 5:
            return HandType.FIVE_OF_A_KIND
        elif max_card == 4:
            return HandType.FOUR_OF_A_KIND
        elif max_card == 3 and second_max_card == 2:
            return HandType.FULL_HOUSE
        elif max_card == 3 and second_max_card < 2:
            return HandType.THREE_OF_A_KIND
        elif max_card == 2 and second_max_card == 2:
            return HandType.TWO_PAIR
        elif max_card == 2 and second_max_card < 2:
            return HandType.ONE_PAIR
        elif high_card:
            return HandType.HIGH_CARD
        raise Exception("Can't find hand type!")

    def translated(self) -> str:
        new_hand = ""
        
        for char in self.hand:
            if char in TRANSLATE:
                new_hand += TRANSLATE[char]
            else:
                new_hand += char
                
        return new_hand

def solve():
    file = open("data/7/data.txt")

    hands = []
    bids = []

    for line in file:
        hand, bid = line.split(" ")

        hands.append(Hand(hand, int(bid.strip())))

    groups = {
        HandType.HIGH_CARD: [],
        HandType.ONE_PAIR: [],
        HandType.TWO_PAIR: [],
        HandType.THREE_OF_A_KIND: [],
        HandType.FULL_HOUSE: [],
        HandType.FOUR_OF_A_KIND: [],
        HandType.FIVE_OF_A_KIND: [],
    }

    for hand in hands:
        groups[hand.hand_type()].append(hand)

    for group in groups:
        groups[group] = sorted(groups[group], key = lambda hand: hand.translated())

    rank = 1
    answer = 0
    
    for group in groups:
        for hand in groups[group]:
            # print(f"{hand} - rank {rank} * bid {hand.bid}")
            answer += rank * hand.bid
            rank += 1

    print(f"Answer 7A: {answer}")
