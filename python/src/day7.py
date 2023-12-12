from enum import Enum
from typing import List

TRANSLATE = {
    "A": "F",
    "K": "E",
    "Q": "D",
    "J": "C",
    "T": "B",
}

TRANSLATE_JOKER = {
    "A": "F",
    "K": "E",
    "Q": "D",
    "J": "1",
    "T": "B",
}

UNTRANSLATE_JOKER = {
    "F": "A",
    "E": "K",
    "D": "Q",
    "1": "J",
    "B": "T",
}

class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

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

    def hand_type_test(self, hand) -> HandType:
        card_dict = {}

        for card in hand:
            if card not in card_dict:
                card_dict[card] = 1
            else:
                card_dict[card] += 1
    
        max_card = max(card_dict.values())

        if max_card < 5:
            second_max_card = sorted(card_dict.values(), reverse=True)[1]
        else:
            second_max_card = 0

        high_card = not any([x for x in card_dict.values() if x > 1])

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

    def joker_type(self) -> HandType:
        if self.hand == "JJ857":
            breakpoint()
    
        most_common_card = max(self.cards, key=self.cards.get)
        highest_card = max(self.translated(joker = True))

        if highest_card in UNTRANSLATE_JOKER:
            highest_card = UNTRANSLATE_JOKER[highest_card]

        if most_common_card == "J":
            most_common_card = highest_card

        new_hand = self.hand.replace("J", most_common_card)

        new_htype = self.hand_type_test(new_hand)

        return new_htype

    def translated(self, joker = False) -> str:
        new_hand = ""
        
        for char in self.hand:
            if not joker:
                if char in TRANSLATE:
                    new_hand += TRANSLATE[char]
                else:
                    new_hand += char
            elif joker:
                if char in TRANSLATE_JOKER:
                    new_hand += TRANSLATE_JOKER[char]
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

    jgroups = {
        HandType.HIGH_CARD: [],
        HandType.ONE_PAIR: [],
        HandType.TWO_PAIR: [],
        HandType.THREE_OF_A_KIND: [],
        HandType.FULL_HOUSE: [],
        HandType.FOUR_OF_A_KIND: [],
        HandType.FIVE_OF_A_KIND: [],
    }

    for hand in hands:
        jgroups[hand.joker_type()].append(hand)

    for jgroup in jgroups:
        jgroups[jgroup] = sorted(jgroups[jgroup], key = lambda hand: hand.translated(joker = True))
        print(jgroups[jgroup])

    rank = 1
    answer = 0
    
    for jgroup in jgroups:
        for hand in jgroups[jgroup]:
            # print(f"{hand} - rank {rank} * bid {hand.bid}")
            answer += rank * hand.bid
            rank += 1

    print(f"Answer 7B: {answer}")
