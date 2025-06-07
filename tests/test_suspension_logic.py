import unittest
from whot import *

class TestSuspensionLogic(unittest.TestCase):

    def test_suspension(self):
        """
        This test checks if the suspension logic works as expected.
        """
        
        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 8)
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

        # Player one plays the pick suspension card
        result = w.play(0)

        # Check suspension result
        self.suspension_result_check(result, "player_1")       

        # Check that the player three is the current player
        self.assertEqual(w.game_state()["current_player"], "player_3")
    
    def test_suspension_disabled(self):
        """
        This test checks suspension logic disabling works
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 8)
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
        w.suspension_enabled = False

        # Start game
        w.start_game()

        # Player one plays the pick holdon card
        result = w.play(0)

        # Check suspension result
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")

        # Check that the player two is the current player
        self.assertEqual(w.game_state()["current_player"], "player_2")

        # Player two goes to market
        w.market()

        # Check if the current player has switched to player three
        self.assertEqual(w.game_state()["current_player"], "player_3")

    def test_suspension_on_game_start(self):
        """
        This test checks if the suspension logic works on game start.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 8)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 3)
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

        # Check that the player two is the current player
        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_suspension_of_last_player(self):
        """
        This test checks if the suspension logic works as expected.
        """
        
        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.WHOT, 20)
        card2 = Card(Suit.CROSS, 3)
        card3 = Card(Suit.TRIANGLE, 11)
        
        card4 = Card(Suit.TRIANGLE, 8)
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

        # Player one plays
        result = w.play(2)

        # Player two plays a suspension card
        result = w.play(0)

        # Check suspension result
        self.suspension_result_check(result, "player_2")

        # Check that the player three is skipped
        self.assertEqual(w.game_state()["current_player"], "player_1")               

    def test_suspension_that_cards_can_be_played_after(self):
        
        """
        This test checks if another card can be played after the suspension card has been played.
        """
        
        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.WHOT, 20)
        card2 = Card(Suit.CROSS, 3)
        card3 = Card(Suit.TRIANGLE, 8)
        
        card4 = Card(Suit.SQUARE, 5)
        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 

        card7 = Card(Suit.STAR, 3)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.TRIANGLE, 11)

        # Create players
        test_players = [ [card1, card2, card3], [card4, card5, card6], [card7, card8, card9] ]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        # Start game
        w.start_game()

        # Player one plays
        result = w.play(2)

        # Check suspension result
        self.suspension_result_check(result, "player_1")

        # Check that the player two is skipped
        self.assertEqual(w.game_state()["current_player"], "player_3")               

        # Player three plays a suspension card
        w.play(2)

        # Check that the player one is the current player
        self.assertEqual(w.game_state()["current_player"], "player_1")

    def test_suspension_that_cards_can_be_played_after_of_different_suit(self):
        
        """
        This test checks if another suit can be played after the suspension card has been played.
        """
        
        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.WHOT, 20)
        card2 = Card(Suit.CROSS, 3)
        card3 = Card(Suit.TRIANGLE, 8)
        
        card4 = Card(Suit.SQUARE, 5)
        card5 = Card(Suit.STAR, 1)
        card6 = Card(Suit.STAR, 2) 

        card7 = Card(Suit.STAR, 3)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.CIRCLE, 8)

        # Create players
        test_players = [ [card1, card2, card3], [card4, card5, card6], [card7, card8, card9] ]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        # Start game
        w.start_game()

        # Player one plays
        result = w.play(2)

        # Check suspension result
        self.suspension_result_check(result, "player_1")

        # Check that the player two is skipped
        self.assertEqual(w.game_state()["current_player"], "player_3")               

        # Player two plays a suspension card
        result = w.play(2)

        # Check suspension result
        self.suspension_result_check(result, "player_3")

        # Check that the player two is the current player
        self.assertEqual(w.game_state()["current_player"], "player_2")

    def suspension_result_check(self, result, player_id):
        """
        Helper function to check the result of a suspension play.
        """

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "suspension")
        self.assertEqual(result["player_id"], player_id)


if __name__ == '__main__':
    unittest.main()