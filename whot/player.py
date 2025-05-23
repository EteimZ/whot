from .deck import Card
from dataclasses import dataclass, asdict

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
    
    def cards(self):
        card_list = []
        for card in self._cards:
            card_list.append(asdict(card))
        
        return card_list

    def receive(self, card: list[Card]):
        self._cards.extend(card)

    def disp(self):
        print(self._cards)
    
    def asdict(self):
        return { "player_id" : self.player_id, "cards": self.cards() }

    def __repr__(self):
        return f"{self.player_id}"

