from enum import Enum

from dataclasses import dataclass
import random

""" Cards (Source Wikipedia)
Circles     1   2   3   4   5      7   8      10  11  12  13  14
Triangles   1   2   3   4   5      7   8      10  11  12  13  14
Crosses     1   2   3       5      7          10  11      13  14
Squares     1   2   3       5      7          10  11      13  14
Stars       1   2   3   4   5      7   8       
5 "Whot" cards numbered 20
"""

CIRCLES_AND_TRIANGLES = [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14]
CROSSES_AND_SQUARES = [1, 2, 3, 5, 7, 10, 11, 13, 14]
STARS = CIRCLES_AND_TRIANGLES[:7]


class Suit(Enum):
    CIRCLE = "circle"
    SQUARE = "square"
    STAR = "star"
    CROSS = "cross"
    TRIANGLE = "triangle"
    WHOT = "whot"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


@dataclass
class Card:
    suit: Suit
    face: int

    # Add a method for equality
    def same(self, other):
        """
        Check if two cards are of the same suit or face
        """
        return self.suit == other.suit or self.face == other.face

    def __hash__(self):
        return hash((self.suit, self.face))

    def __str__(self):
        return f"{self.face} {self.suit.name}"

    def __repr__(self):
        return f"{self.face} {self.suit.name}"


class Deck:
    def __init__(self):
        self.cards = []
        self._create_deck()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self, n: int):
        """
        Deal n amount of cards
        """

        length = len(self.cards)
        if n > length:
            pass

        deal_cards = self.cards[length - n:]
        self.cards = self.cards[: length - n]
        return deal_cards

    def _create_deck(self):
        # Create angle and circle cards
        angles = [Card(Suit.TRIANGLE, angle) for angle in CIRCLES_AND_TRIANGLES]
        circles = [Card(Suit.CIRCLE, circle) for circle in CIRCLES_AND_TRIANGLES]

        # Create cross and square cards
        crosses = [Card(Suit.CROSS, cross) for cross in CROSSES_AND_SQUARES]
        squares = [Card(Suit.SQUARE, square) for square in CROSSES_AND_SQUARES]

        # Create star cards
        stars = [Card(Suit.STAR, star) for star in STARS]

        # Create whot cards
        whots = [Card(Suit.WHOT, 20) for _ in range(5)]

        # Place all cards together
        self.cards.extend(angles + circles + crosses + squares + stars + whots)
    
    def receive_cards(self, cards):
        random.shuffle(cards)
        self.cards = cards
    
    def draw_card(self, card: Card):
        card_index = self.cards.index(card)
        drawn_card = self.cards[card_index]
        del self.cards[card_index]
        return drawn_card
    
    def draw_cards(self, cards: list[Card]):
        drawn_cards = []

        for card in cards:
            drawn_cards.append(self.draw_card(card))
        
        return drawn_cards