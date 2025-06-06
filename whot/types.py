from typing import TypedDict, Literal

from .deck import Card

class CardDict(TypedDict):
    suit: str
    face: int

class EngineResponse(TypedDict):
    status: bool
    type: Literal[
        "request",
        "pick_2",
        "suspension",
        "general_market",
        "pick_3",
        "hold_on",
        "normal"
    ]
    card: CardDict
    player_id: str

class RequestResponse(TypedDict):
    requested_suit: str
    player_id: str

class GameState(TypedDict):
    current_player: str
    pile_top: Card
    players: dict[str, list[Card]]

class GameView(TypedDict):
    current_player: str
    pile_top: Card
    players: dict[str, list[Card] | int ]

class SerializedGameState(TypedDict):
    current_player: str
    pile_top: CardDict
    players: dict[str, list[CardDict]]

class SerializedGameView(TypedDict):
    current_player: str
    pile_top: CardDict
    players: dict[str, list[CardDict] | int]