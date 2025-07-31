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
    
    async def send(self, socket_id, server_event):
        """
        sends message to a particular websocket client
        """

        await self.connections[socket_id].send(json.dumps(server_event))

    async def broadcast(self, server_event, exceptions = None):
        """
        sends message to all websocket client
        """

        # Todo: add exceptions in broadcast

        websockets.broadcast(self.connections.values(), json.dumps(server_event))

@dataclass
class Message:
    receiver_ids: list[str]
    content: str

class WhotServer:

    def __init__(self):
        self.JOIN = {}

    async def start(self, websocket: ClientConnection):

        game = Whot()
        gameConnection = GameConnection(game)

        player_id = gameConnection.add_connection(websocket)

        join_key = secrets.token_urlsafe(4)
        self.JOIN[join_key] = gameConnection

        try:
            server_event = {
                "type": "init",
                "join": join_key
            }

            await websocket.send(json.dumps(server_event))
            await self.play(websocket, game, player_id, gameConnection)
        finally:
            del self.JOIN[join_key]

    async def join(self, websocket: ClientConnection, join_key):
        try:
            gameConnection: GameConnection = self.JOIN[join_key]
            
            server_event = {
                "type": "message",
                "message": "New Player Joined"
            }
            
            player_id = gameConnection.add_connection(websocket)

            await gameConnection.broadcast(server_event)
            
            await self.play(websocket, gameConnection.game, player_id, gameConnection)
            
        except KeyError:
            await websocket.send(json.dumps({
                "type": "message",
                "message": "Invalid join key"
            }))
            await websocket.close()

    async def play(self, websocket: ClientConnection, game: Whot, player_id: str, gameConnection: GameConnection):
        server_event = {
            "type": "start",
            "player_id": player_id,
        }

        await websocket.send(json.dumps(server_event)) 

        while gameConnection.num_of_connections < len(game.players):
            await asyncio.sleep(1)

        game.start_game()

        await self.send_event_to_all("play", game, gameConnection)

        if game.request_mode == True:
            socket_id = game.current_player.player_id
            await self.send_event_to_one(socket_id, "request", game, gameConnection)
        
        async for message in websocket:
            
            client_event = json.loads(message)

            if client_event["type"] == "play":           
                if client_event["player_id"] == game.game_state()["current_player"]:

                    card_index = int(client_event["card"])

                    try:
                        result = game.play(card_index)
                        
                        if result["status"] == True and result["type"] != "request":

                            if result["type"] == "pick_2":
                                await self.handle_pick_two(game, gameConnection)   

                            elif result["type"] == "general_market":
                                await self.handle_general_market(game, gameConnection)
                            
                            elif result["type"] == "suspension":
                                await self.handle_suspension(game, gameConnection)

                            elif result["type"] == "hold_on":
                                await self.handle_hold_on(game, gameConnection)

                            else:
                                message = Message(
                                    receiver_ids=[game.current_player.player_id], 
                                    content="Your turn to play.")
                                
                                await self.send_event_to_all("play", game, gameConnection, message)
                        
                        elif result['type'] == "request":
                            await self.handle_request(game, gameConnection)

                        elif result['status'] == False:

                            await self.send_event_to_all("play", game, gameConnection)
                            
                            server_event = {
                                "type": "win",
                                "winner": result['player_id'],
                            }
                            game.save("game.json") # Todo: This could be improved
                            
                            await gameConnection.broadcast(server_event)
                        
                    except GameNotStartedError:
                        server_event = {
                            "type": "message",
                            "message": "Game has not started yet"
                        }
                        await websocket.send(json.dumps(server_event))

                    except GameOverError:
                        server_event = {
                            "type": "message",
                            "message": "Game is over"
                        }
                        await websocket.send(json.dumps(server_event))

                    except InvalidMoveError:
                        server_event = {
                            "type": "message",
                            "message": "Invalid move"
                        }
                        await websocket.send(json.dumps(server_event))

                    except InvalidCardError:
                        server_event = {
                            "type": "message",
                            "message": "Invalid card"
                        }
                        await websocket.send(json.dumps(server_event))

                    except InvalidSuitError:
                        server_event = {
                            "type": "message",
                            "message": "Invalid suit"
                        }
                        await websocket.send(json.dumps(server_event))

                    except Exception as e:
                        server_event = {
                            "type": "message",
                            "message": f"An error occurred: {str(e)}"
                        }
                        await websocket.send(json.dumps(server_event))

                else:
                    server_event = {
                        "type": "message",
                        "message":"It is not your turn" 
                    }
                    
                    await websocket.send(json.dumps(server_event))

            elif client_event["type"] == "market":
                
                if client_event["player_id"] == game.game_state()["current_player"]:

                    game.market()

                    message = Message(
                        receiver_ids=[game.current_player.player_id], 
                        content="Your turn to play."
                    )
                                
                    await self.send_event_to_all("play",  game, gameConnection, message)

            elif client_event["type"] == "request":
                suit = client_event["suit"]

                requester = game.game_state()['current_player']

                card = str(game.request(suit)['requested_suit'])

                for socket_id in gameConnection.connections:

                    server_event = {
                        "type": "play",
                        "player_id": socket_id,
                        "game_state": serialize_game_view(game.view(socket_id))
                    }

                    await gameConnection.send(socket_id, server_event)

                    if socket_id != requester:
                        server_event = {
                            "type": "message",
                            "message": f"{requester} needs {card}",
                        }

                        await gameConnection.send(socket_id, server_event)

    async def handle_pick_two(self, game: Whot, gameConnection: GameConnection):
        message = Message(
            receiver_ids=[game.current_player.player_id], 
            content="Pick two! You have been asked to pick two cards.")
        
        await self.send_event_to_all("play", game, gameConnection, message)

    async def handle_general_market(self, game: Whot, gameConnection: GameConnection):
        other_players = list(gameConnection.connections.keys())
        other_players.remove(game.current_player.player_id)
    
        message = Message(
            receiver_ids=other_players, 
            content="Everyone Go gen.")
        
        await self.send_event_to_all("play", game, gameConnection, message)

    async def handle_suspension(self, game: Whot, gameConnection: GameConnection):
        try:
            current_player_index = game.players.index(game.current_player) - 1
            suspended_player_id = game.players[current_player_index].player_id
        except IndexError:
            current_player_index = len(game.players) - 1
            suspended_player_id = game.players[current_player_index].player_id
        
        message = Message(
            receiver_ids=[suspended_player_id], 
            content="You have been suspended.")
        
        await self.send_event_to_all("play", game, gameConnection, message)
    
    async def handle_hold_on(self, game: Whot, gameConnection: GameConnection):
        try:
            current_player_index = game.players.index(game.current_player) + 1
            on_hold_player_id = game.players[current_player_index].player_id
        except IndexError:
            current_player_index = 0
            on_hold_player_id = game.players[current_player_index].player_id
        
        message = Message(
            receiver_ids=[on_hold_player_id], 
            content="You have been placed on hold.")
        
        await self.send_event_to_all("play", game, gameConnection, message)

    async def handle_request(self, game: Whot, gameConnection: GameConnection):
        current_player = game.current_player.player_id

        for socket_id in gameConnection.connections:

            server_event = {
                "type": "play",
                "player_id": socket_id,
                "game_state": serialize_game_view(game.view(socket_id))
            }
            
            await gameConnection.send(socket_id, server_event)

            if socket_id == current_player:
                
                server_event = {
                    "type": "request",
                    "player_id": socket_id,
                    "game_state": serialize_game_view(game.view(socket_id))
                }
            
                await gameConnection.send(socket_id, server_event)

    async def send_event_to_all(self, type, game: Whot, gameConnection: GameConnection, message: Message | None = None):
        for socket_id in gameConnection.connections:
            server_event = {
                "type": type,
                "player_id": socket_id,
                "game_state": serialize_game_view(game.view(socket_id))
            }

            await gameConnection.send(socket_id, server_event)

            if message != None:
                if socket_id in message.receiver_ids:
                # Notify the player to pick two cards

                    server_event = {
                        "type": "message",
                        "message": message.content
                    }
                                        
                    await gameConnection.send(socket_id, server_event)

    async def send_event_to_one(self, socket_id, type, game: Whot, gameConnection: GameConnection):
        server_event = {
            "type": type,
            "player_id": socket_id,
            "game_state": serialize_game_view(game.view(socket_id))
        }

        await gameConnection.send(socket_id, server_event)

    async def handle(self, websocket: ClientConnection):
        message = await websocket.recv()
        client_event = json.loads(message)

        assert client_event["type"] == "init"

        if "join" in client_event:
            await self.join(websocket, client_event["join"])
        else:
            await self.start(websocket)