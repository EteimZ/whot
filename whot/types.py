from typing import TypedDict
from .deck import Card

class EngineResponse(TypedDict):
    status: str
    message: str

class GameState(TypedDict):
    current_player: str
    pile_top: Card
    players: dict[str, list[Card]]

class GameView(TypedDict):
    current_player: str
    pile_top: Card
    players: dict[str, list[Card] | int ]