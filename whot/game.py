from .deck import Deck, Card, Suit
from .player import Player
from .utils import serialize_game_state
from .types import EngineResponse
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
            p.receive(deck.deal_card(self.num_of_cards))
        
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

        self._Nigerian_Mode = True
        self._go_gen_enabled = True
        self._pick_two_enabled = True
        self._pick_three_enabled = False
        self._suspension_enabled = True
        self._hold_on_enabled = True

    
    def view(self, player_id):
        """
        Get a view of the game from a player's perspective
        """
        view = {}

        view["current_player"] = self.current_player.player_id
        view["pile_top"] = self.pile[-1]
        view["players"] = {}

        for p in self.players:
            if (p.player_id == player_id):
                view["players"][p.player_id] = p._cards
            else:
                view["players"][p.player_id] = len(p._cards)

        return view
    
    def game_state(self):
        self.current_state = { "current_player": self.current_player.player_id }
        self.current_state["pile_top"] = self.pile[-1]
        self.current_state["players"] = {}

        for p in self.players:
            self.current_state["players"][p.player_id] = p._cards
        
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

            if self.pick_two_enabled:
                if self.pile[0].face == 2:
                    self.pick = 2
                    self.pick_mode = True
            
            if self.pick_three_enabled:
                if self.pile[0].face == 5:
                    self.pick = 3
                    self.pick_mode = True

            if self.suspension_enabled:
                if self.pile[0].face == 8:
                    self._next_player()
            
            if self.go_gen_enabled:
                if self.pile[0].face == 14:
                    self._handle_go_gen()
            
            if self.pile[0].face == 20:
                self.request_mode = True

    @event_storage
    def play(self, card_index: int) -> EngineResponse:
        try:
            if self.initial_play_state == False:
                return {"status": "Error", "message": "Game has not started. Call start_game() to begin."}
            
            self.selected_card: Card = self.current_state['players'][self.current_player.player_id][card_index]
            top_card = self.pile[-1]

            # request card logic
            if (self.selected_card.suit == Suit.WHOT and self.pick_mode == False):
                self.pile.append(self.selected_card)
                self.current_player._cards.remove(self.selected_card)

                if (len(self.current_player._cards) == 0):
                    self.initial_play_state = True
                    return {"status": "GameOver", "message": f"{self.current_player.player_id} has won the game."}
                
                self.request_mode = True
                
                return {"status": "Request", "message": f"{self.current_player.player_id} wants to make a request."}

            if self.request_mode:

                if self.Nigerian_Mode:
            
                    # Hold on logic in request mode
                    if self.hold_on_enabled and ((self.selected_card.suit == self.requested_suit and self.selected_card.face == 1)):
                        self.request_mode = False
                        return self._hold_on_logic()

                    # Go to market logic in request mode
                    if self.go_gen_enabled and ((self.selected_card.suit == self.requested_suit and self.selected_card.face == 14)):
                        self.request_mode = False
                        return self._go_gen_logic()

                    # Suspension logic in request mode
                    if self.suspension_enabled and ((self.selected_card.suit == self.requested_suit and self.selected_card.face == 8)):
                        self.request_mode = False
                        return self._suspension_logic()
                    
                    # pick two logic in request mode
                    if self.pick_two_enabled and ((self.selected_card.suit == self.requested_suit and self.selected_card.face == 2)):
                        self.request_mode = False
                        return self._pick_two_logic()

                    # pick three logic in request mode
                    if self.pick_three_enabled and ((self.selected_card.suit == self.requested_suit and self.selected_card.face == 5)):
                        self.request_mode = False
                        return self._pick_three_logic()

                # whot card logic
                if self.selected_card.suit == self.requested_suit:
                    self.pile.append(self.selected_card)
                    self.current_player._cards.remove(self.selected_card)

                    if (len(self.current_player._cards) == 0):
                        self.initial_play_state = True
                        return {"status": "GameOver", "message": f"{self.current_player.player_id} has won the game."}
                    
                    self._next_player()
                    self.request_mode = False
                    return {"status": "Success", "message": f"{self.current_player.player_id} played {self.selected_card}."}          

                else:
                    return {"status": "Failed", "message": "The card doesn't match the requested suit."}

            if self.Nigerian_Mode:

                if self.pick_mode:
                    if (self.selected_card.face != self.pick):
                        return {"status": "Failed", "message": "The card doesn't match the number."}
                    
                    if (self.selected_card.face == self.pick):
                        self.pile.append(self.selected_card)
                        self.current_player._cards.remove(self.selected_card)
                        
                        if (len(self.current_player._cards) == 0):
                            self.initial_play_state = True
                            return {"status": "GameOver", "message": f"{self.current_player.player_id} has won the game."}                        
                        
                        self.num_of_picks += self.pick
                        self._next_player()

                        return {"status": "Success", "message": f"{self.current_player.player_id} played {self.selected_card}."}

                # Pick two logic       
                if self.pick_two_enabled and ((self.selected_card.face == 2 and self.selected_card.suit == top_card.suit) or (self.selected_card.face == 2 and top_card.face == 2)):
                    return self._pick_two_logic()

                # Pick three logic
                if self.pick_three_enabled and ((self.selected_card.face == 5 and self.selected_card.suit == top_card.suit) or (self.selected_card.face == 5 and top_card.face == 5)):
                    return self._pick_three_logic()

                # Hold on logic
                if self.hold_on_enabled and ((self.selected_card.face == 1 and self.selected_card.suit == top_card.suit) or (self.selected_card.face == 1 and top_card.face == 1)):
                    return self._hold_on_logic()
                
                # Go to market logic
                if self.go_gen_enabled and ((self.selected_card.face == 14 and self.selected_card.suit == top_card.suit) or (self.selected_card.face == 14 and top_card.face == 14)):
                    return self._go_gen_logic()
                
                # Suspension logic
                if self.suspension_enabled and ((self.selected_card.face == 8 and self.selected_card.suit == top_card.suit) or (self.selected_card.face == 8 and top_card.face == 8)):
                    return self._suspension_logic()        

            # normal logic
            if (self.selected_card.face == top_card.face or self.selected_card.suit == top_card.suit ):
                self.pile.append(self.selected_card)
                self.current_player._cards.remove(self.selected_card)

                if (len(self.current_player._cards) == 0):
                    self.initial_play_state = True
                    return {"status": "GameOver", "message": f"{self.current_player.player_id} has won the game."}                        
     
                self._next_player()
                return {"status": "Success", "message": f"{self.current_player.player_id} played {self.selected_card}."}
            
            else:
                return {"status": "Failed", "message": "The card doesn't match the top card suit or face."}
        
        except IndexError:
            return {"status": "Failed", "message": f"Invalid card index: {card_index}. Must be between 0 and {len(self.current_player._cards) - 1}."}


    @event_storage
    def market(self):
        if self.initial_play_state == False:
            return {"status": "Error", "message": "Game has not started. Call start_game() to begin."}
        
        if self.gen.cards == []:
            new_cards = self.pile[:-1]
            self.pile = self.pile[-1:]
            self.gen.receive_cards(new_cards)

        if self.pick_mode:
            received_cards = self.gen.deal_card(self.num_of_picks)
            self.current_player.receive(received_cards)
            self.pick_mode = False
            self.num_of_picks = 2
            self._next_player()

        else:
            received_card = self.gen.deal_card(1)
            self.current_player.receive(received_card)
            self._next_player()

    def request(self, suit):
        if self.initial_play_state == False:
            return {"status": "Error", "message": "Game has not started. Call start_game() to begin."}

        if suit == "whot":
            pass
        else:
            try:
                self.requested_suit = Suit(suit)
                self._next_player()
                return {"requested_suit": self.requested_suit}
            except ValueError:
                return {"status": "Error", "message": f"Invalid suit: {suit}. Must be one of {list(Suit)}."}
    
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
    
    def _next_player(self, skip=1):

        n = self.players.index(self.current_player)
        try:
            self.current_player = self.players[n + skip]
        except IndexError:
            self.current_player = self.players[0]
    
    def _handle_go_gen(self, exempt_player: Player | None = None):
        """
        Method to handle going gen
        """
     
        if exempt_player:
            gen_list = self.players.copy()
            gen_list.remove(exempt_player)
        
            for player in gen_list:
                received_card = self.gen.deal_card(1)
                player.receive(received_card)

        else:
            for player in self.players:
                received_card = self.gen.deal_card(1)
                player.receive(received_card)
    
    def _pick_two_logic(self):
        self.pile.append(self.selected_card)
        self.current_player._cards.remove(self.selected_card)

        if (len(self.current_player._cards) == 0):
            return {"status": "GameOver", "winner":self.current_player.player_id }
                
        self.pick_mode = True
        self.pick = 2
        self._next_player()
        return {"status": f"Pick {self.pick}"}

    def _pick_three_logic(self):
        self.pile.append(self.selected_card)
        self.current_player._cards.remove(self.selected_card)

        if (len(self.current_player._cards) == 0):
            return {"status": "GameOver", "winner":self.current_player.player_id }
                
        self.pick_mode = True
        self.pick = 3
        self._next_player()
        return {"status": f"Pick {self.pick}"}
    
    def _hold_on_logic(self):
        self.pile.append(self.selected_card)
        self.current_player._cards.remove(self.selected_card)

        if (len(self.current_player._cards) == 0):
            return {"status": "GameOver", "winner":self.current_player.player_id }
        
        return {"status": "Success"}     

    def _go_gen_logic(self):
        self.pile.append(self.selected_card)
        self.current_player._cards.remove(self.selected_card)
        self._handle_go_gen(self.current_player)

        if (len(self.current_player._cards) == 0):
            return {"status": "GameOver", "winner":self.current_player.player_id }
        
        self._next_player()
        self._next_player()
        return {"status": "Success"}   

    def _suspension_logic(self):
        self.pile.append(self.selected_card)
        self.current_player._cards.remove(self.selected_card)
                
        if (len(self.current_player._cards) == 0):
            return {"status": "GameOver", "winner":self.current_player.player_id }
                
        self._next_player()
        self._next_player()
        return {"status": "Success"}

    @property
    def Nigerian_Mode(self):
        return self._Nigerian_Mode

    @Nigerian_Mode.setter
    def Nigerian_Mode(self, value):
        if not isinstance(value, bool):
            raise ValueError("Nigerian_Mode must be a boolean value.")

        self._Nigerian_Mode = value

    @property
    def go_gen_enabled(self):
        return self._go_gen_enabled
    
    @go_gen_enabled.setter
    def go_gen_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("go_gen_enabled must be a boolean value.")
        
        self._go_gen_enabled = value
    
    @property
    def pick_two_enabled(self):
        return self._pick_two_enabled

    @pick_two_enabled.setter
    def pick_two_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("pick_two_enabled must be a boolean value.")
        
        self._pick_two_enabled = value

    @property
    def pick_three_enabled(self):
        return self._pick_three_enabled

    @pick_three_enabled.setter
    def pick_three_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("pick_three_enabled must be a boolean value.")
        
        self._pick_three_enabled = value
    
    @property
    def suspension_enabled(self):
        return self._suspension_enabled
    
    @suspension_enabled.setter
    def suspension_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("suspension_enabled must be a boolean value.")
        
        self._suspension_enabled = value
    
    @property
    def hold_on_enabled(self):
        return self._hold_on_enabled
    
    @hold_on_enabled.setter
    def hold_on_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("hold_on_enabled must be a boolean value.")
        
        self._hold_on_enabled = value


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
            self.players[player_id - 1].receive(deck.draw_cards(cards))
        
        self.gen: Deck = deck
        self.current_player: Player = self.players[0]
        self.game_running = True
        self.request_mode = False
        self.requested_suit = None

        self.initial_play_state = False
        
        self.event_store.append(serialize_game_state(self.game_state()))