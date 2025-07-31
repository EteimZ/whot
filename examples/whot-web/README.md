# Web Whot

A web-based implementation of **Whot**. With Web Whot, you can play the game over any network. Just create a game and share the link with another player.

> Currently supports **two players per game**.

## Technologies Used

This project is built using simple, lightweight technologies:

**Client:**

* HTML
* Vanilla JavaScript
* CSS

**Communication:**

* HTTP
* WebSocket (for real-time updates)

**Server:**

* [aiohttp](https://github.com/aio-libs/aiohttp) – HTTP framework for Python
* [whot](https://github.com/EteimZ/whot) – Whot engine that powers the logic

## Getting Started

### 1. Clone the Game Engine

Start by cloning the [`whot`](https://github.com/EteimZ/whot) repository:

```bash
git clone https://github.com/EteimZ/whot.git
cd whot/examples/whot-web
```

### 2. Set Up Your Environment

Make sure you have **Python 3.11+** installed.

(Optional) Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project and define the following variables:

```dotenv
ADDRESS=127.0.0.1
PORT=8080
WEBSOCKET_PORT=8765
```

`ADDRESS` should be your local or network IP address.
`PORT` is for the HTTP server.
`WEBSOCKET_PORT` is for WebSocket communication.

## Running the App

Start the application with:

```bash
python main.py
```

Visit `http://<ADDRESS>:<PORT>` in your browser and start playing.

