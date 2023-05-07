from enum import Enum
from collections import Counter
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
    face: int

    # Add a method for equality

    def __repr__(self):
        return f'{self.face} {self.suit.name}'


class Deck:

    def __init__(self):
        self.cards = []
        self._create_deck()
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self, n: int):
        '''
        Deal n amount of cards
        '''

        length = len(self.cards)
        if n > length:
            pass
        
        deal_cards = self.cards[length-n:]
        self.cards = self.cards[:length-n]
        return deal_cards

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

class Player:
    '''
    A player has:
    1. an id
    2. cards
    3. a method to transfer card(s) 
    4. a method to recieve card(s)
    5. print cards
    '''

    def __init__(self, player_id):
        self._cards = []
        self.player_id = player_id

    def transfer(self, n):
        card = self._cards[n]
        self.cards.remove(card)
        return card

    def recieve(self, card: list[Card]):
        self._cards.extend(card)
        
    def disp(self):
        print(self._cards)

    def __repr__(self):
        return f"{self.player_id}"
        

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
    
    def __init__(self, deck: Deck, players: list[Player]):
        deck.shuffle()
        self.players = players
        for p in self.players:
            p.recieve(deck.deal_card(4))
        self.pile = deck.deal_card(1)
        self.gen = deck
        self.turn = self.players[0]

    def play(self):
        while len(self.players[0]._cards) != 0 and len(self.players[1]._cards) != 0 :
            print(f'Pile: {self.pile[-1]}')
            print(f'{self.turn.player_id}: {self.turn._cards}')
            print()
            inp = int(input("Please input card index or -1 to go gen: "))
            if inp == -1:
                self.turn.recieve(self.gen.deal_card(1))
            else:
                try:
                    if self.turn._cards[inp].face == self.pile[-1].face or self.turn._cards[inp].suit == self.pile[-1].suit:
                        self.pile.append(self.turn._cards[inp])
                        self.turn._cards.remove(self.turn._cards[inp])
                    
                        if self.pile[-1].face == 2:
                            print(f"{self.opposite(self.turn)} Pick two: ")
                            other_player = self.opposite(self.turn)
                            recieved_card = self.gen.deal_card(2)
                            print(f"{self.opposite(self.turn.player_id)} you recieved: {recieved_card}")
                            other_player.recieve(recieved_card)

                        if self.pile[-1].face == 14:
                            print(f"{self.opposite(self.turn.player_id)} Go Gen: ")
                            other_player = self.opposite(self.turn)
                            recieved_card = self.gen.deal_card(1)
                            print(f"{self.opposite(self.turn.player_id)} you recieved: {recieved_card}")
                            other_player.recieve(recieved_card)
                    
                        if self.pile[-1].face == 8:
                            # temporary logic
                            print(f"{self.opposite(self.turn.player_id)} has been suspended: ")
                            self.swap(self.turn)
                    
                        if self.pile[-1].face == 1:
                            # add an edge case to check if the player provides a another one
                            # Add logic to catch when 1 is the last card
                            print(f"{self.opposite(self.turn.player_id)} Hold on: ")
                            inp = int(input(f"{self.turn.player_id} Please input any card index of your choice: "))
                            self.pile.append(self.turn._cards[inp])
                            self.turn._cards.remove(self.turn._cards[inp])
                            print(f"{self.opposite(self.turn.player_id)} Resume")
                        '''
                        if self.pile[-1] == Card(Suit.WHOT, 20):
                            print(f"{self.turn.player_id} ask {self.opposite(self.turn.player_id)} for any card of your choice")
                            face = input(f"Face of the card: ")
                            suit = input(f"Face of the card: ")
                        '''
                    else:
                        print("Card doesn't match top of pile")
                        self.swap(self.turn)

                except IndexError:
                    print("You are out of order. Try again")
                    self.swap(self.turn)

        
            self.swap(self.turn)

        print(f"{self.turn} you win.")

    def swap(self, current_player):
        if current_player == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
    
    def opposite(self, current_player):
        if current_player == self.players[0]:
            return self.players[1]
        else:
            return self.players[0]





p = Player("Eteims")
p2 = Player("Jacob")


d = Deck()
g = Game(d, [p, p2])
g.play()
