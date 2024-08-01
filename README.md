# Whot

An implementation of the [Whot](https://en.wikipedia.org/wiki/Whot!) game (Nigerian variation). The app is a web application that currently uses vanilla JS for the frontend and Python for the backend. The communication protocol used for the application is [WebSocket](https://en.wikipedia.org/wiki/WebSocket).

## Background 

Whot is a popular card game played across Nigeria. It can be played by two or more players. There's a predefined set of rules that have to be followed for a player to win the game. The winner of the game is the person who doesn't have any cards left in their hand.

## Usage

To use this you need `Python 3.11` or higher. Other lower versions of Python might work but I haven't tested them.

First, install the dependencies with this command:

```bash
pip install -r requirements.txt
```

Then run the server:

```bash
python3 server.py
```

To run the frontend you can use any webserver of your choice. I am using python's web server:

```bash
python -m http.server
```

The application would be running on `127.0.0.1:8000`.


## Contributions

This code base is open to contributions. To contribute, check out the [issues](https://github.com/EteimZ/whot/issues) of the repo. Pick an issue you want to resolve and drop a comment to express your interest in resolving the issue. If there's no issue, you can create an issue that you can resolve yourself or let someone else resolve it.

If you want to make contributions, first you have to fork the repo. Make your changes to your fork, then open a PR.
