from enum import Enum
from dataclasses import dataclass
import random

''' Cards (Source Wikipedia)
Circles     1   2   3   4   5       7   8       10  11  12  13  14
Triangles   1   2   3   4   5       7   8       10  11  12  13  14
Crosses     1   2   3       5       7           10  11      13  14
Squares     1   2   3       5       7           10  11      13  14
Stars       1   2   3   4   5       7   8                    
5 "Whot" cards numbered 20
'''

CIRCLES_AND_TRIANGLES = [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14]
CROSSES_AND_SQUARES = [ 1, 2, 3, 5, 7, 10, 11, 13, 14]
STARS = CIRCLES_AND_TRIANGLES[:7]


class Suit(Enum):
    CIRCLE = 0
    SQUARE = 1
    STAR = 2
    CROSS = 3
    ANGLE = 4
    WHOT = 5

    def __repr__(self):
        return f'{self.name}'

@dataclass
class Card:
    suit: Suit
    value: int


class Deck:

    def __init__(self):
        self.cards = []
        self._create_deck()
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(n: int):
        '''
        Deal n amount of cards
        '''
        pass


    def _create_deck(self):

        # Create angle and circle cards
        angles = [ Card(Suit.ANGLE, angle) for angle in CIRCLES_AND_TRIANGLES ]
        circles = [ Card(Suit.CIRCLE, circle) for circle in CIRCLES_AND_TRIANGLES ]

        # Create cross and square cards
        crosses = [ Card(Suit.CROSS, cross) for cross in CROSSES_AND_SQUARES ]
        squares = [ Card(Suit.SQUARE, square) for square in CROSSES_AND_SQUARES ]

        # Create star cards

        stars = [ Card(Suit.STAR, star) for star in STARS ]
        
        # Create whot cards
        whots = [ Card(Suit.WHOT, 20) for _ in range(5) ]

        # Place all cards together
        self.cards.extend(angles + circles + crosses + squares + stars + whots)

@dataclass
class Player:
    '''
    A player has:
    1. an id
    2. cards
    3. a method to give card(s) 
    4. a method to recieve card(s)
    '''
    cards: list[Card]
    player_id : int 

        

class Game:
    '''
    A game has:
    1. A deck of cards.
    2. Two players(currently) with pile of six cards each.
    3. A General market
    4. A pile
    5. A instance variable keeping track of turns
    6. Rules defining the game of whots
    '''
    pass



d = Deck()
print(len(d.cards))
d.shuffle()
print(d.cards)
