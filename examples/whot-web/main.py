import asyncio
import os

from aiohttp import web
import aiohttp_jinja2
from dotenv import load_dotenv
import jinja2
from websockets.asyncio.server import serve

from server import handler

load_dotenv()

ADDRESS = os.environ.get("ADDRESS", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8080))
WEBSOCKET_PORT = int(os.environ.get("WEBSOCKET_PORT", 8765))

# Create an aiohttp web app
app = web.Application()

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('.'))

# Serve index.html
async def handle_index(request):
    return web.FileResponse("index.html")

async def handle_game(request):
    return aiohttp_jinja2.render_template("game.html", request, context={
        "websocket_url": f"ws://{ADDRESS}:{WEBSOCKET_PORT}"
    })

# WebSocket server function
async def websocket_server():
    async with serve(handler, ADDRESS, WEBSOCKET_PORT):
        print(f"WebSocket server running at ws://{ADDRESS}:{WEBSOCKET_PORT}")
        await asyncio.Future()  # Keep the WebSocket server running

# Define routes
app.router.add_get("/", handle_index)
app.router.add_get("/game", handle_game)
app.router.add_static("/", path=".", name="static")

# Function to run the aiohttp server
async def run_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, ADDRESS, PORT)
    print(f"HTTP server running at http://{ADDRESS}:{PORT}")
    await site.start()
    await asyncio.Future()  # Keep running

# Run both WebSocket and HTTP server concurrently
async def main():
    await asyncio.gather(websocket_server(), run_server())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shut down by user.")
