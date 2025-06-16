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
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 4)

        
        # Check that the player one is the current player
        self.assertEqual(w.game_state()["current_player"], "player_1")

    def test_go_gen_on_game_start(self):

        """
        This test checks go gen logic when the game starts with pick two as pile card.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 14)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 3)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 2)
        card4 = Card(Suit.WHOT, 20)

        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 

        card7 = Card(Suit.STAR, 3)
        card8 = Card(Suit.STAR, 4)

        # Create players
        test_players = [[card1, card2], [card3, card4], [card5, card6], [card7, card8]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        # Start game
        w.start_game()

        # Run assertions
        self.assertEqual(len(w.game_state()["players"]["player_1"]), 3)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 3)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 3)
        self.assertEqual(len(w.game_state()["players"]["player_4"]), 3)

        self.assertEqual(w.game_state()["current_player"], "player_1")

    def test_go_gen_disable(self):

        """
        This test checks the go gen logic can be properly disabled.
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

        # disable pick two
        w.go_gen_enabled = False

        # Start game
        w.start_game()

        # Player go gen card
        w.play(0)


        self.assertEqual(len(w.game_state()["players"]["player_1"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 3)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 3)

        self.assertEqual(w.game_state()["current_player"], "player_2")


if __name__ == "__main__":
    unittest.main()