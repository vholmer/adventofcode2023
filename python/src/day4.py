import re

from typing import (
    List,
    Any,
)

class Card:
    n: int
    winning: List[int]
    owned: List[int]
    winrefs: List[int]

    def __init__(self, n, winning, owned):
        self.n = n
        self.winning = winning
        self.owned = owned
        self.winrefs = self._get_winrefs()

    def __str__(self):
        return f"""Card {self.n}:
Winning: {self.winning}
Owned: {self.owned}
Points: {self.points()}
Wins: {self.num_wins()}
Winrefs: {self.winrefs}
-------------"""

    def points(self) -> int:     
        return int(2 ** (self.num_wins() - 1))

    def num_wins(self) -> List[int]:
        return sum([1 for x in self.winning if x in self.owned])

    def _get_winrefs(self) -> List[int]:
        return [1 + x for x in range(self.n, self.n + self.num_wins())]

    def process(self, cards: List[Any], cardcount = 1, depth = 0) -> int:
        # Including this card in cardcount by default value
        for winref in self.winrefs:
            cardcount += cards[winref - 1].process(cards, 1, depth + 1)
        
        return cardcount

def solve():
    file = open("data/4/data.txt")

    result = 0

    cards = []

    for line in file:
        n = int(line.split(':')[0].replace('Card ', '').strip())
    
        card = line.split(':')[1].strip()

        winning = card.split(' | ')[0].strip()
        owned = card.split(' | ')[1].strip()

        winning = re.sub(r'\s+', ',', winning)
        owned = re.sub(r'\s+', ',', owned)

        winning = sorted([int(x) for x in winning.split(',')])
        owned = sorted([int(x) for x in owned.split(',')])

        card = Card(n, winning, owned)

        cards.append(card)

        result += card.points()

    cards.sort(key = lambda card: card.n)

    cardcount = 0

    for card in cards:
        cardcount += card.process(cards)

    print(f"Answer 4A: {result}")
    print(f"Answer 4B: {cardcount}")
