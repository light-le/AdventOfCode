from collections import Counter, namedtuple
from utils import AdventSession, extract_year_day_from_path

session = AdventSession(**extract_year_day_from_path(__file__))

from enum import Enum

CardBid = namedtuple('CardBid', ['card_set', 'bid'])

CARDS = 'A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2'
CARDS2 = 'A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J'


class CardSet:
    def __init__(self, cards: str, card_str: str=CARDS) -> None:
        self.cards = cards
        self.sorted_cards = card_str.split(', ')[::-1]
    
    def __gt__(self, o) -> bool:
        for card_a, card_b in zip(self.cards, o.cards):
            if self.sorted_cards.index(card_a) > self.sorted_cards.index(card_b):
                return True
            elif self.sorted_cards.index(card_a) < self.sorted_cards.index(card_b):
                return False
        return False
    
    def __lt__(self, o) -> bool:
        for card_a, card_b in zip(self.cards, o.cards):
            if self.sorted_cards.index(card_a) < self.sorted_cards.index(card_b):
                return True
            elif self.sorted_cards.index(card_a) > self.sorted_cards.index(card_b):
                return False
        return False

class SetType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1
    
def determine_set_type(cards: str) -> SetType:
    card_counter = Counter(cards)
    if len(card_counter) == 1:
        return SetType.FIVE_OF_A_KIND
    elif len(card_counter) == 2:
        if 4 in card_counter.values():
            return SetType.FOUR_OF_A_KIND
        else:
            return SetType.FULL_HOUSE
    elif len(card_counter) == 3:
        if 3 in card_counter.values():
            return SetType.THREE_OF_A_KIND
        else:
            return SetType.TWO_PAIR
    elif len(card_counter) == 4:
        return SetType.ONE_PAIR
    else:
        return SetType.HIGH_CARD
    
def determine_set_type2(cards: str) -> SetType:
    card_counter = Counter(cards)
    count_J = card_counter['J']
    
    if len(card_counter) == 1:
        return SetType.FIVE_OF_A_KIND
    elif len(card_counter) == 2:
        if 'J' in card_counter:
            return SetType.FIVE_OF_A_KIND
        elif 4 in card_counter.values():
            return SetType.FOUR_OF_A_KIND
        else:
            return SetType.FULL_HOUSE
    elif len(card_counter) == 3:
        if 3 in card_counter.values():
            if count_J == 3 or count_J == 1: # can only be either 3 or 1, not 2
                return SetType.FOUR_OF_A_KIND
            return SetType.THREE_OF_A_KIND
        else:
            if count_J == 2:
                return SetType.FOUR_OF_A_KIND
            elif count_J == 1:
                return SetType.FULL_HOUSE
            return SetType.TWO_PAIR
    elif len(card_counter) == 4:
        if count_J > 0:
            return SetType.THREE_OF_A_KIND
        return SetType.ONE_PAIR
    else:
        if count_J:
            return SetType.ONE_PAIR
        return SetType.HIGH_CARD


@session.submit_result(level=1, tests=[({'inp': [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483'
]}, 6440)], print_only=False)
def solve_part1(inp: list[str]):
    
    card_bids = []
    for line in inp:
        cardset, bid = line.split()
        card_bids.append(CardBid(CardSet(cardset), int(bid)))
    
    sorted_sets = sorted(card_bids, key=lambda cs: (determine_set_type(cs.card_set.cards).value, cs.card_set))
    winnings = [ss.bid * i for i, ss in enumerate(sorted_sets, start=1)]
    return sum(winnings)
    

@session.submit_result(level=2, tests=[({'inp': [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483'
]}, 5905)], print_only=False)
def solve_part2(inp: list[str]):
    card_bids = []
    for line in inp:
        cardset, bid = line.split()
        card_bids.append(CardBid(CardSet(cardset, card_str=CARDS2), int(bid)))
    
    sorted_sets = sorted(card_bids, key=lambda cs: (determine_set_type2(cs.card_set.cards).value, cs.card_set))
    winnings = [ss.bid * i for i, ss in enumerate(sorted_sets, start=1)]
    return sum(winnings)


if __name__ == '__main__':
    inp = session.read_input().split('\n')[:-1]
    
    solve_part1(inp)
    
    solve_part2(inp)
