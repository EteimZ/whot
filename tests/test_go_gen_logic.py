import unittest
from whot import *
from whot.exceptions import InvalidCardError

class TestGoGenLogic(unittest.TestCase):
    
    def test_go_gen(self):
        """
        This test checks if the go gen logic works as expected.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 14)
        card2 = Card(Suit.CROSS, 3)
        card3 = Card(Suit.TRIANGLE, 11)
        
        card4 = Card(Suit.WHOT, 20)
        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 

        card7 = Card(Suit.STAR, 3)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.SQUARE, 5)

        # Create players
        test_players = [ [card1, card2, card3], [card4, card5, card6], [card7, card8, card9] ]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        # Start game
        w.start_game()

        # Player one plays the go gen card
        w.play(0)

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 4)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 3)

        
        # Check that the player one is the current player
        self.assertEqual(w.game_state()["current_player"], "player_3")

if __name__ == "__main__":
    unittest.main()