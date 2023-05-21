"""
TODO: Create a client to use the game and remove usage logic from the game class
FIXME: Fix all edge cases in the whot method
TODO: Refactor the Game class
TODO: Handle when first card on pile is special card
"""
from enum import Enum

# from collections import Counter
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
    CIRCLE = 0
    SQUARE = 1
    STAR = 2
    CROSS = 3
    ANGLE = 4
    WHOT = 5

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
        angles = [Card(Suit.ANGLE, angle) for angle in CIRCLES_AND_TRIANGLES]
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


class Player:
    """
    A player has:
    1. an id
    2. cards
    3. a method to transfer card(s)
    4. a method to recieve card(s)
    5. print cards
    """

    def __init__(self, player_id):
        self._cards: list[Card] = []
        self.player_id: int = player_id

    def transfer(self, n):
        card = self._cards[n]
        self._cards.remove(card)
        return card

    def recieve(self, card: list[Card]):
        self._cards.extend(card)

    def disp(self):
        print(self._cards)

    def __repr__(self):
        return f"{self.player_id}"


class Game:
    """
    A game has:
    1. A deck of cards.
    2. Two players(currently) with pile of six cards each.
    3. A General market
    4. A pile
    5. A instance variable keeping track of turns
    6. Rules defining the game of whots
    """

    def __init__(self, deck: Deck, players: list[Player]):
        deck.shuffle()
        self.players: list[Player] = players
        for p in self.players:
            p.recieve(deck.deal_card(3))
        self.pile: list[Card] = deck.deal_card(1)
        self.gen = deck
        self.current_player: Player = self.players[0]

    def play(self):
        while True:
            print(f"Pile: {self.pile[-1]}")
            print(f"{self.current_player.player_id}: {self.current_player._cards}")
            print()
            inp = int(input("Please input card index or -1 to go gen: "))
            if inp == -1:
                self.current_player.recieve(self.gen.deal_card(1))
            else:
                try:
                    if (
                        self.current_player._cards[inp].same(self.pile[-1])
                        or self.current_player._cards[inp].suit == Suit.WHOT
                    ):
                        self.pile.append(self.current_player._cards[inp])
                        self.current_player._cards.remove(
                            self.current_player._cards[inp]
                        )

                        if self.pile[-1].face == 2:
                            self.handle_pick_two()

                        if self.pile[-1].face == 14:
                            self.handle_go_gen()

                        if self.pile[-1].face == 8:
                            self.handle_suspension()

                        if self.pile[-1].face == 1:
                            self.handle_hold_on()

                        if self.pile[-1] == Card(Suit.WHOT, 20):
                            self.handle_whot()

                    else:
                        print("Card doesn't match top of pile")
                        self.swap()

                except IndexError:
                    print("You are out of order. Try again")
                    self.swap()

            if self.check_winner():
                break

            self.swap()

        print(f"{self.current_player} you win.")    

    def handle_pick_two(self):
        """
        Method to handle giving players pick two
        """
        next_player = self.next_player()

        print(f"{next_player} Pick two: ")
        recieved_card = self.gen.deal_card(2)
        next_player.recieve(recieved_card)
        print(f"{next_player} you recieved: {recieved_card}")

    def handle_go_gen(self):
        """
        Method to handle going gen
        """

        next_player = self.next_player()

        print(f"{next_player} Go Gen: ")
        recieved_card = self.gen.deal_card(1)
        next_player.recieve(recieved_card)
        print(f"{next_player} you recieved: {recieved_card}")

    def handle_suspension(self):
        """
        Method to handle suspension
        """
        next_player = self.next_player()

        print(f"{next_player} has been suspended: ")
        self.swap()
    
    def handle_hold_on(self):
        """
        Method to handle hold on
        """

        next_player = self.next_player()

        print(f"{next_player} Hold on: ")
        print(f"{self.current_player._cards}")
        inp = int(
            input(f"{self.current_player} Please input any card index of your choice: ")
        )
        self.pile.append(self.current_player._cards[inp])
        self.current_player._cards.remove(self.current_player._cards[inp])
        if self.pile[-1].face == 1:
            self.handle_hold_on()
        if self.pile[-1].face == 14:
            self.handle_go_gen()
        if self.pile[-1].face == 8:
            self.handle_suspension()
            return
        if self.pile[-1].face == 2:
            self.handle_pick_two()
        if self.pile[-1] == Card(Suit.WHOT, 20):
            self.handle_whot()
        if self.current_player._cards == []:
            print(f"{self.current_player} you win")
            return
        print(f"{next_player} Resume")

    def handle_whot(self):
        """
        Method to handle whot card
        """

        next_player = self.next_player()

        print(
            f"{self.current_player} ask {next_player}  for any card suit of your choice"
        )
        suit = input("Suit of the card(STAR, CIRCLE, ANGLE, SQUARE, CROSS): ")
        print(f"{next_player._cards}")
        inp = int(input(f"{next_player} select a card with suit of {suit}: "))
        returned_card = next_player._cards[inp]

        if str(returned_card.suit) == suit:
            next_player._cards.remove(returned_card)
            self.pile.append(returned_card)
            self.swap()
        else:
            print(f"{next_player} doesn't have the card. You go gen")
            next_player.recieve(self.gen.deal_card(1))
            print(f"{next_player} you recieved: {next_player._cards[-1]}")
            print(f"{self.current_player} play any card of your choice: ")
            print(f"{self.current_player._cards}")
            inp = int(input("Please input card index: "))
            self.pile.append(self.current_player._cards[inp])
            self.current_player._cards.remove(self.current_player._cards[inp])

    def check_winner(self):
        """
        This function will be used to check the winner of the game 
        based on who doesn't hac
        """
        for player in self.players:
            if len(player._cards) == 0:
                return True
        return False

    def swap(self):
        n = self.players.index(self.current_player)
        try:
            self.current_player = self.players[n + 1]
        except IndexError:
            self.current_player = self.players[0]

    def next_player(self):
        n = self.players.index(self.current_player)
        try:
            return self.players[n + 1]
        except IndexError:
            return self.players[0]


p1 = Player("Eteims")
p2 = Player("Jacob")
p3 = Player("Ted")

d = Deck()
g = Game(d, [p1, p2, p3])
g.play()
