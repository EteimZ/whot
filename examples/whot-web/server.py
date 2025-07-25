import asyncio
import websockets
from websockets.asyncio.client import ClientConnection
from whot import Whot
from whot.utils import serialize_game_view
from whot.exceptions import (
    GameNotStartedError,
    GameOverError,
    InvalidMoveError,
    InvalidCardError,
    InvalidSuitError,
)

import json
import secrets

from dataclasses import dataclass

# Todo:
# Consider adding everything to a class
# Work on individual messages in the play event. Done
# Work on disconnections so users can that get disconnected can always reconnect
# The game ends when all players have left, Add option for restart
# Refactor code Done

# 

JOIN = {}


class GameConnection:
    """
    This class stores the created instance of the game
    it's connections
    The number of players that have joined    
    """

    def __init__(self, game: Whot):
        self.game = game
        self.connections: dict[str, ClientConnection] = {}
        self.num_of_connections = 0
    
    def add_connection(self, connection: ClientConnection) -> str:
        if len(self.game.players) != self.num_of_connections:
            self.num_of_connections += 1
            self.connections[f"player_{self.num_of_connections}"] = connection
            return f"player_{self.num_of_connections}"
        else:
            return False
    
    async def send(self, socket_id, event):
        """
        sends message to a particular websocket client
        """

        await self.connections[socket_id].send(json.dumps(event))

    async def broadcast(self, event, exceptions = None):
        """
        sends message to all websocket client
        """

        websockets.broadcast(self.connections.values(), json.dumps(event)) # type: ignore

@dataclass
class Message:
    receiver_ids: list[str]
    content: str

class WhotServer:
    async def play(self):
        pass
    
    async def handler(self):
        pass

    async def start(self):
        pass

    async def join(self):
        pass

    async def send_event_to_all(self):
        pass

    async def send_event_to_one(self):
        pass

async def send_event_to_all( type, game: Whot, gameConnections: GameConnection, message: Message | None = None):
    for socket_id in gameConnections.connections:
        event = {
            "type": type,
            "player_id": socket_id,
            "game_state": serialize_game_view(game.view(socket_id))
        }

        await gameConnections.send(socket_id, event)

        if message != None:
            if socket_id in message.receiver_ids:
            # Notify the player to pick two cards

                event = {
                    "type": "message",
                    "message": message.content
                }
                                    
                await gameConnections.send(socket_id, event)

async def send_event_to_one(socket_id, type, game: Whot, gameConnections: GameConnection):
    event = {
        "type": type,
        "player_id": socket_id,
        "game_state": serialize_game_view(game.view(socket_id))
    }

    await gameConnections.send(socket_id, event)



async def play(websocket: ClientConnection, game: Whot, player_id: str, gameConnections: GameConnection):
    event = {
        "type": "player_id",
        "player_id": player_id,
    }

    await websocket.send(json.dumps(event)) 

    while gameConnections.num_of_connections < len(game.players):
        await asyncio.sleep(1)

    game.start_game()

    await send_event_to_all("play", game, gameConnections)

    if game.request_mode == True:
        socket_id = game.current_player.player_id
        await send_event_to_one(socket_id, "request", game, gameConnections)
    
    async for message in websocket:
        
        event = json.loads(message)

        if event["type"] == "play":           
            if event["player_id"] == game.game_state()["current_player"]:

                card_index = int(event["card"])

                try:
                    result = game.play(card_index)
                    
                    if result["status"] == True and result["type"] != "request":

                        if result["type"] == "pick_2":

                            message = Message(
                                receiver_ids=[game.current_player.player_id], 
                                content="Pick two! You have been asked to pick two cards.")
                            
                            await send_event_to_all(result["type"], game, gameConnections, message)

                        elif result["type"] == "general_market":

                            other_players = list(gameConnections.connections.keys())
                            other_players.remove(game.current_player.player_id)
                        
                            message = Message(
                                receiver_ids=other_players, 
                                content="Everyone Go gen.")
                            
                            await send_event_to_all(result["type"], game, gameConnections, message)
                        
                        elif result["type"] == "suspension":
                            try:
                                current_player_index = game.players.index(game.current_player) - 1
                                suspended_player_id = game.players[current_player_index].player_id
                            except IndexError:
                                current_player_index = len(game.players) - 1
                                suspended_player_id = game.players[current_player_index].player_id
                            
                            message = Message(
                                receiver_ids=[suspended_player_id], 
                                content="You have been suspended.")
                            
                            await send_event_to_all(result["type"], game, gameConnections, message)

                        elif result["type"] == "hold_on":
                            try:
                                current_player_index = game.players.index(game.current_player) + 1
                                on_hold_player_id = game.players[current_player_index].player_id
                            except IndexError:
                                current_player_index = 0
                                on_hold_player_id = game.players[current_player_index].player_id
                            
                            message = Message(
                                receiver_ids=[on_hold_player_id], 
                                content="You have been placed on hold.")
                            
                            await send_event_to_all(result["type"], game, gameConnections, message)

                        else:

                            message = Message(
                                receiver_ids=[game.current_player.player_id], 
                                content="Your turn to play.")
                            
                            await send_event_to_all(result["type"], game, gameConnections, message)
                    
                    elif result['type'] == "request":

                        current_player = game.current_player.player_id

                        for socket_id in gameConnections.connections:

                            if socket_id == current_player:
                                
                                event = {
                                    "type": "request",
                                    "player_id": socket_id,
                                    "game_state": serialize_game_view(game.view(socket_id))
                                }

                            else:

                                event = {
                                    "type": "play",
                                    "player_id": socket_id,
                                    "game_state": serialize_game_view(game.view(socket_id))
                                }
                            
                            await gameConnections.send(socket_id, event)

                    elif result['status'] == False:

                        await send_event_to_all(result["type"], game, gameConnections)
                        
                        event = {
                            "type": "win",
                            "winner": result['player_id'],
                        }
                        game.save("game.json") # Todo: This could be improved
                        
                        await gameConnections.broadcast(event)
                       
                except GameNotStartedError:
                    event = {
                        "type": "message",
                        "message": "Game has not started yet"
                    }
                    await websocket.send(json.dumps(event))

                except GameOverError:
                    event = {
                        "type": "message",
                        "message": "Game is over"
                    }
                    await websocket.send(json.dumps(event))

                except InvalidMoveError:
                    event = {
                        "type": "message",
                        "message": "Invalid move"
                    }
                    await websocket.send(json.dumps(event))

                except InvalidCardError:
                    event = {
                        "type": "message",
                        "message": "Invalid card"
                    }
                    await websocket.send(json.dumps(event))

                except InvalidSuitError:
                    event = {
                        "type": "message",
                        "message": "Invalid suit"
                    }
                    await websocket.send(json.dumps(event))

                except Exception as e:
                    event = {
                        "type": "message",
                        "message": f"An error occurred: {str(e)}"
                    }
                    await websocket.send(json.dumps(event))

            else:
                event = {
                    "type": "message",
                    "message":"It is not your turn" 
                }
                
                await websocket.send(json.dumps(event))

        elif event["type"] == "market":
            
            if event["player_id"] == game.game_state()["current_player"]:

                game.market()

                message = Message(
                    receiver_ids=[game.current_player.player_id], 
                    content="Your turn to play."
                )
                            
                await send_event_to_all("play", game, gameConnections, message)
                    

        elif event["type"] == "request":
            suit = event["suit"]

            requester = game.game_state()['current_player']

            card = str(game.request(suit)['requested_suit'])

            for socket_id in gameConnections.connections:

                if socket_id != requester:
                    event = {
                        "type": "request_card",
                        "message": f"{requester} requested for {card}",
                        "game_state": serialize_game_view(game.view(socket_id))
                    }

                    await gameConnections.send(socket_id, event)

async def join(websocket: ClientConnection, join_key):
    try:
        gameConnection: GameConnection = JOIN[join_key]
        
        event = {
            "type": "message",
            "message": "New Player Joined"
        }
        
        await gameConnection.broadcast(event)
        
        player_id = gameConnection.add_connection(websocket)

        await play(websocket, gameConnection.game, player_id, gameConnection)
        
    except KeyError:
        await websocket.send(json.dumps({
            "type": "message",
            "message": "Invalid join key"
        }))
        await websocket.close()


async def start(websocket: ClientConnection):

    # These values would defined by the client later
    num_of_player = 2
    num_of_cards = 4

    game = Whot(num_of_player, num_of_cards)
    
    gameConnection = GameConnection(game)
    player_id = gameConnection.add_connection(websocket)

    join_key = secrets.token_urlsafe(4)
    JOIN[join_key] = gameConnection

    try:
        event = {
            "type": "init",
            "join": join_key
        }

        await websocket.send(json.dumps(event))
        await play(websocket, game, player_id, gameConnection)
    finally:
        del JOIN[join_key]

async def handler(websocket: ClientConnection):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"
    if "join" in event:
        await join(websocket, event["join"])
    else:
        await start(websocket)