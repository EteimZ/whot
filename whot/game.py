from .deck import Deck, Card, Suit
from .player import Player
from .utils import serialize_game_state
import json
import uuid
import os


class Engine:

    def __init__(self, number_of_players: int = 2, number_of_cards: int = 4):
        """
        This would be used to configure the whot engine.
        """

        self.num_of_players = number_of_players
        self.num_of_cards = number_of_cards
        self.event_store = []

        # Create deck and shuffle
        deck = Deck()
        deck.shuffle()

        # Create players
        self.players: list[Player] = []
        for i in range(self.num_of_players):
            self.players.append(Player(f"player_{i + 1}"))
        
        for p in self.players:
            p.recieve(deck.deal_card(self.num_of_cards))
        
        self.pile: list[Card] = deck.deal_card(1)
        self.gen: Deck = deck
        self.current_player: Player = self.players[0]
        self.game_running = True
        self.request_mode = False
        self.requested_suit = None
        self.pick_mode = False
        self.num_of_picks = 2

        self.initial_play_state = False

        self.event_store.append(serialize_game_state(self.game_state()))

        self.Nigerian_Mode = True

        """
        British Mode
        Enable Pick 3
        """
    
    def view(self, player_id):
        """
        Get a view of the game from a player's perspective
        """
        view = {}

        view["current_player"] = self.current_player.player_id
        view["pile_top"] = self.pile[-1]

        for p in self.players:
            if (p.player_id == player_id):
                view[p.player_id] = p._cards
            else:
                view[p.player_id] = len(p._cards)

        return view
    
    def game_state(self):
        self.current_state = { "current_player": self.current_player.player_id }
        self.current_state["pile_top"] = self.pile[-1]

        for p in self.players:
            self.current_state[p.player_id] = p._cards
        
        return self.current_state

    @staticmethod
    def event_storage(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            event = serialize_game_state(self.game_state())
            if len(self.event_store) >=  1:
                if self.event_store[-1] == event:
                    return result
                self.event_store.append(event)  
                return result
        return wrapper    

    @event_storage
    def start_game(self):

        if self.initial_play_state == False:
            self.initial_play_state = True

            if self.pile[0].face == 2:
                self.pick_mode = True

            if self.pile[0].face == 8:
                self.next_player()
            
            if self.pile[0].face == 14:
                self.handle_go_gen()
            
            if self.pile[0].face == 20:
                self.request_mode = True

    @event_storage
    def play(self, card_index: int):

        selected_card: Card = self.current_state[self.current_player.player_id][card_index]
        top_card = self.pile[-1]

        # request card logic
        if (selected_card.suit == Suit.WHOT and self.pick_mode == False):
            self.pile.append(selected_card)
            self.current_player._cards.remove(selected_card)

            if (len(self.current_player._cards) == 0):
                return {"status": "GameOver", "winner":self.current_player.player_id }
            
            self.request_mode = True
            
            return {"status": "Request"}

        if self.request_mode:

            if self.Nigerian_Mode:

                # Hold on logic in request mode
                if (selected_card.suit == self.requested_suit and selected_card.face == 1):
                    self.pile.append(selected_card)
                    self.current_player._cards.remove(selected_card)
                    
                    if (len(self.current_player._cards) == 0):
                        return {"status": "GameOver", "winner":self.current_player.player_id }
                    
                    self.request_mode = False
                    return {"status": "Success"}

                # Go to market logic in request mode
                if selected_card.suit == self.requested_suit and selected_card.face == 14:
                    self.pile.append(selected_card)
                    self.current_player._cards.remove(selected_card)

                    self.handle_go_gen(self.current_player)

                    if (len(self.current_player._cards) == 0):
                        return {"status": "GameOver", "winner":self.current_player.player_id }
                    
                    self.next_player()
                    self.next_player()
                    self.request_mode = False

                    return {"status": "Success"}

                # Suspension logic in request mode
                if selected_card.suit == self.requested_suit and selected_card.face == 8:
                    self.pile.append(selected_card)
                    self.current_player._cards.remove(selected_card)
                
                    if (len(self.current_player._cards) == 0):
                        return {"status": "GameOver", "winner":self.current_player.player_id }
                    
                    self.next_player()
                    self.next_player()
                    self.request_mode = False
                    return {"status": "Success"}
                
                # pick two logic in request mode
                if selected_card.suit == self.requested_suit and selected_card.face == 2:
                    self.pile.append(selected_card)
                    self.current_player._cards.remove(selected_card)

                    if (len(self.current_player._cards) == 0):
                        return {"status": "GameOver", "winner":self.current_player.player_id }
                
                    self.pick_mode = True
                    self.pick = 2
                    self.next_player()
                    return {"status": f"Pick {self.pick}"}

            # whot card logic
            if selected_card.suit == self.requested_suit:
                self.pile.append(selected_card)
                self.current_player._cards.remove(selected_card)

                if (len(self.current_player._cards) == 0):
                    return {"status": "GameOver", "winner":self.current_player.player_id }
                
                self.next_player()
                self.request_mode = False
                return {"status": "Success"}              

            else:
                return {"status": "Failed"}

        if self.Nigerian_Mode:

            if self.pick_mode:
                if (selected_card.face != self.pick):
                    return {"status": "Failed"}
                
                if (selected_card.face == self.pick):
                    self.pile.append(selected_card)
                    self.current_player._cards.remove(selected_card)
                    
                    if (len(self.current_player._cards) == 0):
                        return {"status": "GameOver", "winner":self.current_player.player_id }
                    
                    
                    self.num_of_picks += self.pick
                    self.next_player()

                    return {"status": "Success"}

            # Pick two logic
            if (selected_card.face == 2 and selected_card.suit == top_card.suit) or (selected_card.face == 2 and top_card.face == 2):
                self.pile.append(selected_card)
                self.current_player._cards.remove(selected_card)

                if (len(self.current_player._cards) == 0):
                    return {"status": "GameOver", "winner":self.current_player.player_id }
                
                self.pick_mode = True
                self.pick = 2
                self.next_player()
                return {"status": f"Pick {self.pick}"}


            # Hold on logic
            if (selected_card.face == 1 and selected_card.suit == top_card.suit) or (selected_card.face == 1 and top_card.face == 1):
                self.pile.append(selected_card)
                self.current_player._cards.remove(selected_card)
                if (len(self.current_player._cards) == 0):
                    return {"status": "GameOver", "winner":self.current_player.player_id }
                return {"status": "Success"}
            
            # Go to market logic
            if (selected_card.face == 14 and selected_card.suit == top_card.suit) or (selected_card.face == 14 and top_card.face == 14):
                self.pile.append(selected_card)
                self.current_player._cards.remove(selected_card)
                self.handle_go_gen(self.current_player)

                if (len(self.current_player._cards) == 0):
                    return {"status": "GameOver", "winner":self.current_player.player_id }
                
                self.next_player()
                self.next_player()
                return {"status": "Success"}
            
            # Suspension logic
            if (selected_card.face == 8 and selected_card.suit == top_card.suit) or (selected_card.face == 8 and top_card.face == 8):
                self.pile.append(selected_card)
                self.current_player._cards.remove(selected_card)
                
                if (len(self.current_player._cards) == 0):
                    return {"status": "GameOver", "winner":self.current_player.player_id }
                
                self.next_player()
                self.next_player()
                return {"status": "Success"}                 

        # normal logic
        if (selected_card.face == top_card.face or selected_card.suit == top_card.suit ):
            self.pile.append(selected_card)
            self.current_player._cards.remove(selected_card)

            if (len(self.current_player._cards) == 0):
                return {"status": "GameOver", "winner":self.current_player.player_id }
                        
            self.next_player()
            return {"status": "Success"}
        
        else:
            return {"status": "Failed"}

    @event_storage
    def market(self):
        
        if self.gen.cards == []:
            new_cards = self.pile[:-1]
            self.pile = self.pile[-1:]
            self.gen.receive_cards(new_cards)

        if self.pick_mode:
            recieved_cards = self.gen.deal_card(self.num_of_picks)
            self.current_player.recieve(recieved_cards)
            self.pick_mode = False
            self.num_of_picks = 2
            self.next_player()

        else:
            recieved_card = self.gen.deal_card(1)
            self.current_player.recieve(recieved_card)
            self.next_player()

    def request(self, suit):
        if suit == "whot":
            pass
        else:
            try:
                self.requested_suit = Suit(suit)
                self.next_player()
                return {"requested_suit": self.requested_suit}
            except ValueError:
                # Handle the case where card_index doesn't match any Suit
                pass
    
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
    
    def handle_go_gen(self, exempt_player: Player | None = None):
        """
        Method to handle going gen
        """
     
        if exempt_player:
            gen_list = self.players.copy()
            gen_list.remove(exempt_player)
        
            for player in gen_list:
                recieved_card = self.gen.deal_card(1)
                player.recieve(recieved_card)

        else:
            for player in self.players:
                recieved_card = self.gen.deal_card(1)
                player.recieve(recieved_card)
    
    def handle_pick_two(self, player: Player | list[Player]):
        """
        Method to handle giving players pick two
        """
        recieved_card = self.gen.deal_card(2)
        player.recieve(recieved_card)

    
    def save(self, path):
        """
        Appends a new game event to the JSON file while preserving existing data.
        """

        game = {
            "id": str(uuid.uuid4()),
            "moves": self.event_store
        }

        # Check if file exists and has content
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]  # Convert old format to list
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(game)  # Append new game

        with open(path, "w") as f:
            json.dump(data, f, indent=4)  # Pretty-print JSON for readability

        return True
    
    def british_mode(self):
        self.Nigerian_Mode = False



class TestEngine(Engine):

    """
    Test Whot Engine
    """
    
    def __init__(self, test_pile_card: Card, test_players: list[list[Card]]):
        """
        In test mode you can set the top pile and players cards.
        """

        self.event_store = []

        deck = Deck()
        deck.shuffle()

        # create test pile
        self.pile: list[Card] = []
        self.pile.append(deck.draw_card(test_pile_card))

        # Create test player 
        self.players: list[Player] = []

        for player_id, cards in enumerate(test_players, start=1):
            self.players.append(Player(f"player_{player_id}"))
            self.players[player_id - 1].recieve(deck.draw_cards(cards))
        
        self.gen: Deck = deck
        self.current_player: Player = self.players[0]
        self.game_running = True
        self.request_mode = False
        self.requested_suit = None

        self.initial_play_state = False
        
        self.event_store.append(serialize_game_state(self.game_state()))