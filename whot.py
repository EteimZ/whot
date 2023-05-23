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
        self.gen: Deck = deck
        self.current_player: Player = self.players[0]

    def play(self):
        self.initial_process()
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

                        self.process()

                    else:
                        print("Card doesn't match top of pile")
                        self.next_player()

                except IndexError:
                    print("You are out of order. Try again")
                    self.next_player()

            if self.check_winner():
                break

            self.next_player()

        print(f"{self.current_player} you win.")

    def initial_process(self):
        """
        This method handles what will happen to the initial player
        If the card on the top of the file is a special one.
        """

        current_player = self.current_player
        next_player = self.next_player()

        if self.pile[-1].face == 2:
            # The current player should pick two
            self.handle_pick_two(current_player)

        if self.pile[-1].face == 14:
            # All players should go gen
            self.handle_go_gen()

        if self.pile[-1].face == 8:
            # The current player should be suspended
            self.handle_suspension(current_player)
    
        if self.pile[-1].face == 1:
            # The current player can play any card of their choice
            self.handle_hold_on(next_player)

        if self.pile[-1] == Card(Suit.WHOT, 20):
            self.handle_whot(next_player)

    def process(self):
        """
        This method handles what will happen during the normal game process
        """

        current_player = self.current_player
        next_player = self.next_player()
        
        if self.pile[-1].face == 2:
            # The next player should pick two cards
            self.handle_pick_two(next_player)

        if self.pile[-1].face == 14:
            # All players should go gen except the current player
            self.handle_go_gen(current_player)

        if self.pile[-1].face == 8:
            # Suspend the next player
            self.handle_suspension(next_player)

        if self.pile[-1].face == 1:
            # The next player should hold on for the current player
            self.handle_hold_on(next_player)

        if self.pile[-1] == Card(Suit.WHOT, 20):
            # The next player should give the current player any card of their choice 
            self.handle_whot(next_player)
            

    def handle_pick_two(self, player: Player):
        """
        Method to handle giving players pick two
        """
        # get_next_player = self.get_next_player()

        print(f"{player} Pick two: ")
        recieved_card = self.gen.deal_card(2)
        player.recieve(recieved_card)
        print(f"{player} you recieved: {recieved_card}")

    def handle_go_gen(self, exempt_player: Player | None = None):
        """
        Method to handle going gen
        """

        # current_player = self.current_player
        
        if exempt_player:
            gen_list = self.players.copy()
            gen_list.remove(exempt_player)
        
            print(f"All players except {exempt_player} Go Gen: ")
            for player in gen_list:
                recieved_card = self.gen.deal_card(1)
                player.recieve(recieved_card)
                print(f"{player} you recieved: {recieved_card}")

        else:
            print(f"Everyone Go Gen: ")
            for player in self.players:
                recieved_card = self.gen.deal_card(1)
                player.recieve(recieved_card)
                print(f"{player} you recieved: {recieved_card}")


    def handle_suspension(self, get_next_player: Player):
        """
        Method to handle suspension
        """

        # get_next_player = self.get_next_player()

        print(f"{get_next_player} has been suspended: ")
        self.next_player()
    
    def handle_hold_on(self, get_next_player: Player):
        """
        Method to handle hold on
        """

        # get_next_player = self.get_next_player()
        
        print(f"{get_next_player} Hold on: ")
        print(f"{self.current_player._cards}")
        inp = int(
            input(f"{self.current_player} Please input any card index of your choice: ")
        )
        self.pile.append(self.current_player._cards[inp])
        self.current_player._cards.remove(self.current_player._cards[inp])
        if self.pile[-1].face == 1:
            self.handle_hold_on(get_next_player)
        if self.pile[-1].face == 14:
            self.handle_go_gen(self.current_player)
        if self.pile[-1].face == 8:
            self.handle_suspension(get_next_player)
            return
        if self.pile[-1].face == 2:
            self.handle_pick_two(get_next_player)
        if self.pile[-1] == Card(Suit.WHOT, 20):
            self.handle_whot(get_next_player)
        if self.current_player._cards == []:
            print(f"{self.current_player} you win")
            return
        print(f"{get_next_player} Resume")

    def handle_whot(self, get_next_player: Player):
        """
        Method to handle whot card
        """

        # get_next_player = self.get_next_player()

        print(
            f"{self.current_player} ask {get_next_player}  for any card suit of your choice"
        )
        suit = input("Suit of the card(STAR, CIRCLE, ANGLE, SQUARE, CROSS): ")
        print(f"{get_next_player._cards}")
        inp = int(input(f"{get_next_player} select a card with suit of {suit}: "))
        returned_card = get_next_player._cards[inp]

        if str(returned_card.suit) == suit:
            get_next_player._cards.remove(returned_card)
            self.pile.append(returned_card)
            self.next_player()
        else:
            print(f"{get_next_player} doesn't have the card. You go gen")
            get_next_player.recieve(self.gen.deal_card(1))
            print(f"{get_next_player} you recieved: {get_next_player._cards[-1]}")
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

    def next_player(self, skip=1):
        n = self.players.index(self.current_player)
        try:
            self.current_player = self.players[n + skip]
        except IndexError:
            self.current_player = self.players[0]

    def get_next_player(self):
        n = self.players.index(self.current_player)
        try:
            return self.players[n + 1]
        except IndexError:
            return self.players[0]


p1 = Player("Eteims")
p2 = Player("Jacob")
# p3 = Player("Ted")

d = Deck()
g = Game(d, [p1, p2])
g.play()
