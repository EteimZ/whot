from .types import GameState, GameView, SerializedGameView, SerializedGameState

def serialize_game_state(game_state: GameState) -> SerializedGameState:
    state: SerializedGameState = {
        "current_player": game_state['current_player'],
        "pile_top": {'suit': str(game_state['pile_top'].suit), 'face': game_state['pile_top'].face },
        "players": {}
    }
    
    for player in game_state['players']:
        state['players'][player] = [{'suit': str(card.suit), 'face': card.face } for card in game_state['players'][player]]

    return state

def serialize_game_view(view: GameView) -> SerializedGameView:
    state: SerializedGameView = {
         "current_player": view['current_player'],
         "pile_top": {'suit': str(view['pile_top'].suit), 'face': view['pile_top'].face },
         "players": {}

    }

    for player in view['players']:
        if type(view['players'][player]) != int:
            state['players'][player] = [{'suit': str(card.suit), 'face': card.face } for card in view['players'][player]]
        
        if type(view['players'][player]) == int:
             state['players'][player] = view['players'][player]

    return state