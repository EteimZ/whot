WHOT
====

**Whot** is an Engine that implements the game of `Whot! <https://en.wikipedia.org/wiki/Whot!>`_
Using this engine, you can build your own Whot! game servers and connect it to any frontend technology of your choice.

.. note::

   This project is under active development.

Installation
------------

The Engine is implemented in python, so to install it, you can use `pip <https://pypi.org/project/pip>`_:

.. code-block:: console

   pip install whot

Once installed, you can start using the engine in your Python projects.

Usage
-----

The engine provides simple set of APIs that corresponds to the actual Whot! game.

To start the game, import the ``Whot`` class

.. code-block:: python
   
   from whot import Whot


Once it is imported, create an instance of the class and start the game:

.. code-block:: python

   game = Whot()

To view the state of the game, use the ``game_state`` method of the class:

.. code-block:: python

   game.game_state()

The ``game_state`` method returns a dictionary that contains the current state of the game:

.. code-block:: python

   {
    'current_player': 'player_1', 
    'pile_top': 13 CIRCLE, 
    'player_1': [3 CIRCLE, 2 STAR, 8 CIRCLE, 5 CIRCLE], 
    'player_2': [7 CIRCLE, 3 SQUARE, 11 CROSS, 8 STAR]
   }

To view the state of the game use from a player's perspective, use the `view` method:

.. code-block:: python

   game.view('player_2')

The code above views the game state from the perspective of ``player_2``:

.. code-block:: python

   {
    'current_player': 'player_1', 
    'pile_top': 13 CIRCLE, 
    'player_1': 4, 
    'player_2': [7 CIRCLE, 3 SQUARE, 11 CROSS, 8 STAR]
   }

To play a card, use the ``play`` method. This method allows you to select which of the current player's cards to play.


Player one, who is the current player, can play any of their cards provided it matches the suit or face of the pile card.

.. code-block:: python

   game.play(0)

If they don't have a playable card, they can use the ``market`` method to draw a new card:

.. code-block:: python

   game.market()


.. toctree::

    ref

.. The table contents is most likely going to be:
   Getting Started
   Concepts
      Engines
      Agents
   Tutorials
      Build a CLI Whot! game
      Create a Websocket server for Whot!
      Build a full stack Whot! game
   API Reference
   Contributing

