<div align="center">

  <img src="https://raw.githubusercontent.com/EteimZ/whot/refs/heads/main/logo.png" alt="whot" />

  <br>

  <a href="https://pypi.org/project/whot" target="_blank">
      <img src="https://img.shields.io/pypi/v/whot.svg?color=red" alt="Package version">
  </a>

  <a href="https://github.com/EteimZ/whot/blob/main/LICENSE">    
      <img src="https://img.shields.io/pypi/l/whot.svg" alt="License">
  </a>

</div>


**WHOT** is an implementation of the [Whot!](https://en.wikipedia.org/wiki/Whot!) game. It is an engine that implements all the necessary logic to implement your whot game.  

## Installation

**WHOT** is implemented in Python. You can easily install it from PyPI using pip:

```bash
pip install whot
```

## Getting Started

The engine's API simulates how the actual whot game is played. 

First you need to import the library:

```python
from whot import Whot 
```

Then create an instance of the engine:

```python
game = Whot()
```

Call the `start_game` method to begin the game:

```python
game.start_game()
```

When the game is started, you can view the current state of the game with the `game_state` method.

```python
game.game_state()
```

This returns:

```python
{'current_player': 'player_1',
 'pile_top': 3 CIRCLE,
 'players': {'player_1': [4 CIRCLE, 13 CROSS, 4 STAR, 2 TRIANGLE],
             'player_2': [5 STAR, 10 CIRCLE, 1 SQUARE, 20 WHOT]}}
```

The game state has the following parameters:
- `current_player`: The player who's turn it is.
- `pile_top`: The card on the top of the pile.
- `players`: A dictionary that contains all the players as keys and their cards as values

If you wish to get the view of a particular player, you can call the `view` method and specify the player's ID.

```python
game.view('player_1')
```

This returns:

```python
{'current_player': 'player_1',
 'pile_top': 3 CIRCLE,
 'players': {'player_1': [4 CIRCLE, 13 CROSS, 4 STAR, 2 TRIANGLE],
             'player_2': 4}}
```

Now, with this, we can begin playing. To play a card, you can use the `play` method to select the index of the current player's card, which in this case is `player_1`.

```python
game.play(0)
```

This plays the first card of the player. When this method is called, the state of the engine updates:

```python
{'current_player': 'player_2',
 'pile_top': 4 CIRCLE,
 'players': {'player_1': [13 CROSS, 4 STAR, 2 TRIANGLE],
             'player_2': [5 STAR, 10 CIRCLE, 1 SQUARE, 20 WHOT]}}
```

The second player, `player_2`, plays their second card.

```python
game.play(1)
```

This also updates the state of the engine again:

```python
{'current_player': 'player_1',
 'pile_top': 10 CIRCLE,
 'players': {'player_1': [13 CROSS, 4 STAR, 2 TRIANGLE],
             'player_2': [5 STAR, 1 SQUARE, 20 WHOT]}}
```

It's player_1's turn again, but they don't have a playable card, so they have to go to market using the `market` method.

```python
game.market()
```

This adds an additional card to player one and switches the turn to player 2:

```python
{'current_player': 'player_2',
 'pile_top': 10 CIRCLE,
 'players': {'player_1': [13 CROSS, 4 STAR, 2 TRIANGLE, 1 CROSS],
             'player_2': [5 STAR, 1 SQUARE, 20 WHOT]}}
```

Player two also doesn't have a playable card, but they have a **whot card**, so they play it:

```python
game.play(2)
```

This puts the game in **request mode**. In request mode, the player who played the whot card can request any card suit of their choice using the **request** method.

```python
game.request('square')
```

Player two requests a `square`. Player one doesn't have it, so they have to go to market.



Go through the [documentation](https://whot.readthedocs.io/en/latest/) to learn more.

## Contributions

This code base is open to contributions. To contribute, check out the [issues](https://github.com/EteimZ/whot/issues) of the repo. Pick an issue you want to resolve and drop a comment to express your interest in resolving the issue. If there's no issue, you can create an issue that you can resolve yourself or let someone else resolve it.

If you want to contribute, first fork the repo. Make your changes to your fork, then open a pull request (PR).