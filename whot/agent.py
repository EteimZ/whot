from abc import ABC, abstractmethod
from collections import Counter
from .game import Engine
from .deck import Suit

class BaseAgent(ABC):
    
    def __init__(self, agent_id, engine):
        self.agent_id = agent_id
        self.engine = engine
    
    @abstractmethod
    def play(self):
        """
        Play the game
        """
        pass


class Agent(BaseAgent):
    """
    An agent can play the game
    """

    def play(self) -> dict:
        """
        Play the game
        """
        game_state = self.engine.game_state()

        # Play whot Card first if the agent has it
        for i, card in enumerate(game_state["players"][self.agent_id]):
            if card.suit == Suit.WHOT:
                cards = Counter([card.suit for card in game_state["players"][self.agent_id] if card.suit != Suit.WHOT])
                requested_card = cards.most_common(1)[0][0]

                result = self.engine.play(i)
                print(result)
                result = self.engine.request(requested_card)
                print(result)
                return

        if self.engine.request_mode == True:
            for i, card in enumerate(game_state["players"][self.agent_id]):
                if card.suit == self.engine.requested_suit:
                    result = self.engine.play(i)
                    print(result)
                    return

        for i, card in enumerate(game_state["players"][self.agent_id]):
            if card.suit == game_state['pile_top'].suit or card.face == game_state['pile_top'].face:
                # Play the card
                result = self.engine.play(i)
                print(result)
                return

        self.engine.market()

        