import unittest
from whot import *
from whot.exceptions import InvalidCardError

class TestHoldOnLogic(unittest.TestCase):
    
    def test_hold_on(self):

        """
        This test checks if hold on logic works as expected.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 1)
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

        # Player one plays the pick holdon card
        w.play(0)

        # Check that the player one is the current player
        self.assertEqual(w.game_state()["current_player"], "player_1")

        # Player one plays another card
        w.play(1)

        # Check if the current player has switched to player two
        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_hold_on_market(self):

        """
        This test checks if hold on logic works as expected when a player goes to market.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 1)
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

        # Player one plays the pick holdon card
        w.play(0)

        # Check that the player one is the current player
        self.assertEqual(w.game_state()["current_player"], "player_1")

        # Player one goes to market
        w.market()

        # Check if the current player has switched to player two
        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_hold_on_disabled(self):

        """
        This test checks hold on logic disabling works.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 1)
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

        # Disable hold on
        w.hold_on_enabled = False

        # Start game
        w.start_game()

        # Player one plays the pick holdon card
        w.play(0)

        # Check that the player two is the current player
        self.assertEqual(w.game_state()["current_player"], "player_2")

        # Player two goes to market
        w.market()

        # Check if the current player has switched to player three
        self.assertEqual(w.game_state()["current_player"], "player_3")

    def test_hold_on_raises_error_when_user_plays_a_different_card_suit_and_face(self):

        """
        This test checks if hold on logic works as expected when a player goes to market.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 1)
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

        # Player one plays the pick hold on card
        w.play(0)

        # Check that the player one is the current player
        self.assertEqual(w.game_state()["current_player"], "player_1")

        # Player one goes to market
        with self.assertRaises(InvalidCardError):
            w.play(0)

        # Check if the current player has switched to player two
        self.assertEqual(w.game_state()["current_player"], "player_1")

        # Go to market
        w.market()

        # Check if the current player has switched to player two
        self.assertEqual(w.game_state()["current_player"], "player_2")
    
    def test_hold_on_double(self):

        """
        This test checks if hold on logic works as expected.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 1)
        card2 = Card(Suit.CROSS, 1)
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

        # Player one plays the pick holdon card
        w.play(0)

        # Check that the player one is the current player
        self.assertEqual(w.game_state()["current_player"], "player_1")

        # Player one plays another holdon card
        w.play(0)

        # Check if the current player has switched to player two
        self.assertEqual(w.game_state()["current_player"], "player_1")

if __name__ == '__main__':
    unittest.main()