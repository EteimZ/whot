import unittest
from whot import *
from whot.exceptions import InvalidCardError

class TestPickTwoLogic(unittest.TestCase):

    def test_pick_two(self):

        """
        This test checks if the pick two logic works as expected.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 2)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 1)
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

        # Player one plays the pick two card
        result = w.play(0)

        # Check if the result is correct
        self.pick_two_result_check(result, "player_1")

        # Check if the engine is in pick mode
        self.assertEqual(w.pick_mode, True)

        # Player two goes to market 
        w.market()

        # Check if the engine is no longer pick mode
        self.assertEqual(w.pick_mode, False)

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 1)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 4)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_4"]), 2)

        self.assertEqual(w.game_state()["current_player"], "player_3")


    def test_pick_two_defend(self):

        """
        This test checks the pick two logic defence.
        When a player plays a pick two the next player can defend it.
        When it is defended the cards the pick two goes to the next player.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 2)
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

        # Player one plays the pick two card
        result = w.play(0)

        # Check if the result is correct
        self.pick_two_result_check(result, "player_1")

        # Check if the engine is in pick mode
        self.assertEqual(w.pick_mode, True)

        # Player two defends
        w.play(0)

        # Still check if the engine is in pick mode
        self.assertEqual(w.pick_mode, True)

        # Player three goes to market 
        w.market()

        # Check if the engine is no longer in pick mode
        self.assertEqual(w.pick_mode, False)

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 1)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 1)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 6)
        self.assertEqual(len(w.game_state()["players"]["player_4"]), 2)

        self.assertEqual(w.game_state()["current_player"], "player_4")

    def test_pick_two_disable(self):

        """
        This test checks the pick two logic can be properly disabled.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 2)
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

        # disable pick two
        w.pick_two_enabled = False

        # Start game
        w.start_game()

        # Player one plays a card with face 2
        w.play(0)

        # Check if the engine is not in pick mode
        self.assertEqual(w.pick_mode, False)

        # Player two plays a card with face 2
        w.play(0)

        # Player three goes to market
        w.market()

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 1)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 1)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 3)
        self.assertEqual(len(w.game_state()["players"]["player_4"]), 2)

        self.assertEqual(w.game_state()["current_player"], "player_4")

    def test_pick_two_on_game_start(self):

        """
        This test checks game logic when the game starts with pick two as pile card.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 2)

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

        # Check if the engine is in pick mode
        self.assertEqual(w.pick_mode, True)

        # Player one goes to market
        w.market()

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 4)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_4"]), 2)

        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_pick_two_on_game_start_defend(self):

        """
        This test checks if the first player can defend if the game starts with a pick two card.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 2)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 2)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.TRIANGLE, 1)
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

        # Check if the engine is in pick mode
        self.assertEqual(w.pick_mode, True)

        # Player one defends
        w.play(0)

        # Player two goes to market
        w.market()

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 1)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 6)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_4"]), 2)

        self.assertEqual(w.game_state()["current_player"], "player_3")

    def test_pick_two_logic_raises_error_when_a_different_face_card_is_played(self):

        """
        This test checks if the game raises an error if a different card is played other than a two
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 4)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 2)
        card2 = Card(Suit.WHOT, 20)

        card3 = Card(Suit.CIRCLE, 5)
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

        # Player one defends
        w.play(0)

        # Check if the engine is in pick mode
        self.assertEqual(w.pick_mode, True)

        # Player two goes to market
        with self.assertRaises(InvalidCardError):
            w.play(0)

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 1)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_4"]), 2)

        self.assertEqual(w.game_state()["current_player"], "player_2")

    def pick_two_result_check(self, result, player_id):
        """
        Helper function to check the result of a suspension play.
        """

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "pick_2")
        self.assertEqual(result["player_id"], player_id)

if __name__ == '__main__':
    unittest.main()