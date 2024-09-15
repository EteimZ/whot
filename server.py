import asyncio
import websockets
from websockets.asyncio.server import serve
from websockets.asyncio.client import ClientConnection

from whot import Whot

import json
import secrets


JOIN = {}

class GameConnection:
    """
    This class stores the created instance of the game
    it's connections
    The number of players that have joined    
    """

    def __init__(self, game: Whot):
        self.game = game
        self.connections: list[ClientConnection] = []
        self.num_of_connections = 0
    
    def add_connection(self, connection: ClientConnection):
        if self.game.num_of_players != self.num_of_connections:
            self.num_of_connections += 1
            self.connections.append(connection)
            return f"player_{self.num_of_connections}"
        else:
            return False

async def play(websocket: ClientConnection, game: Whot, player_id: str, gameConnections: GameConnection):

    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "play"

        card_index = event["card"]

        
        game.play(card_index)

        websockets.broadcast(gameConnections.connections, json.dumps(game.current_state))

async def join(websocket: ClientConnection, join_key):
    try:
        gameConnection: GameConnection = JOIN[join_key]
    except KeyError:
        print("Game doesn't exist")
        return

    player_id = gameConnection.add_connection(websocket)

    await play(websocket, gameConnection.game, player_id, gameConnection)

async def start(websocket: ClientConnection):
    game = Whot(2, number_of_cards=4)
    gameConnection = GameConnection(game)
    player_id = gameConnection.add_connection(websocket)

    join_key = secrets.token_urlsafe(12)
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

async def main():
    async with serve(handler, "localhost", 8765):
        print("Server running on: localhost:8765")
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shut down by user.")
