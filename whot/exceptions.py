class WhotEngineError(Exception):
    """Base exception for all Whot engine errors."""
    pass

class GameNotStartedError(WhotEngineError):
    """Raised when an action is attempted before the game starts."""
    pass

class GameOverError(WhotEngineError):
    """Raised when an action is attempted after the game is over."""
    pass

class InvalidMoveError(WhotEngineError):
    """Raised when a player attempts an invalid move."""
    pass


class InvalidCardError(WhotEngineError):
    """Raised when an invalid card is played or referenced."""
    pass

class InvalidSuitError(WhotEngineError):
    """Raised when an invalid suit is requested."""
    pass