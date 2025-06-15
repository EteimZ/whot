import unittest
from whot import *
from whot.exceptions import InvalidCardError


class TestWhotEngine(unittest.TestCase):
    """
    ## Test Play
    Test the game won't play unless the game has started
    Test the game won't continue if it is game over
    Test if the game raises invalid card error if the card suit doesn't match
    Test if the game raises invalid card error if the card face doesn't match
    Test if the game raises invalid move error if the selected card isn't within the player's index
    
    ## Test Market
    Test that a players card increases when they go to market
    Test that market won't work when the game hasn't started
    Test that market won't work if the game is over

    # Test Misc
    Test the save functionalilty
    Test restart functionality (TODO: implement restart functionality)
    """
    def test_play_suit(self):
        """
        Test to see if a card of the same suit can be played.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 4)
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

        # Player one plays card
        result = w.play(0)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")


        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_play_face(self):
        """
        Test to see if a card of the same face can be played.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.SQUARE, 3)
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

        # Player one plays card
        result = w.play(0)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")

        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_british_mode_hold_on(self):
        """
        Test to see hold on doesn't work in british mode.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 1)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 2)

        card6 = Card(Suit.CIRCLE, 4)
        card7 = Card(Suit.TRIANGLE, 13)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.SQUARE, 3)
        card10 = Card(Suit.CROSS, 11)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        w.Nigerian_Mode = False

        # Start game
        w.start_game()

        # Player one plays the pick two card
        result = w.play(0)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")


        self.assertEqual(w.game_state()["current_player"], "player_2")        

    def test_british_mode_pick_two(self):
        """
        Test to see pick two doesn't work in british mode.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CIRCLE, 4)
        card7 = Card(Suit.TRIANGLE, 13)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.SQUARE, 3)
        card10 = Card(Suit.CROSS, 11)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        w.Nigerian_Mode = False

        # Start game
        w.start_game()

        # Player one plays the pick two card
        result = w.play(0)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")

        w.market()

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 4)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 6)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 5)

        self.assertEqual(w.game_state()["current_player"], "player_3")        

    def test_british_mode_pick_three(self):
        """
        Test to see pick two doesn't work in british mode.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 5)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CIRCLE, 4)
        card7 = Card(Suit.TRIANGLE, 13)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.SQUARE, 3)
        card10 = Card(Suit.CROSS, 11)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        w.Nigerian_Mode = False

        # Start game
        w.start_game()

        # Player one plays the pick two card
        result = w.play(0)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")

        w.market()

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 4)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 6)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 5)

        self.assertEqual(w.game_state()["current_player"], "player_3")

    def test_british_mode_suspension(self):
        """
        Test to see suspension doesn't work in british mode.
        """

        # Define top pile card
        pile = Card(Suit.STAR, 7)

        # Define player cards
        card1 = Card(Suit.STAR, 8)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CIRCLE, 4)
        card7 = Card(Suit.TRIANGLE, 13)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.SQUARE, 3)
        card10 = Card(Suit.CROSS, 11)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        w.Nigerian_Mode = False

        # Start game
        w.start_game()

        # Player one plays the pick two card
        result = w.play(0)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")

        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_british_mode_go_gen(self):
        """
        Test to see suspension doesn't work in british mode.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 14)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.CIRCLE, 5)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CIRCLE, 4)
        card7 = Card(Suit.TRIANGLE, 13)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.SQUARE, 3)
        card10 = Card(Suit.CROSS, 11)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        w.Nigerian_Mode = False

        # Start game
        w.start_game()

        # Player one plays the pick two card
        result = w.play(0)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 4)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 5)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 5)

        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_british_request(self):
        """
        Test to see if you can make request in british mode.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.CIRCLE, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CIRCLE, 4)
        card7 = Card(Suit.TRIANGLE, 13)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.SQUARE, 3)
        card10 = Card(Suit.CROSS, 11)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        w.Nigerian_Mode = False

        # Start game
        w.start_game()

        # Player one plays the pick two card
        result = w.play(1)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "request")
        self.assertEqual(result["player_id"], "player_1")


        # Check if the engine is in request mode
        self.assertTrue(w.request_mode)

        # Check the current player is still player one despite playing the whot card
        self.assertEqual(w.game_state()["current_player"], "player_1")

        # request for circle 
        request_result = w.request("circle")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "circle")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")
        
        # Check if an error is raised if the player plays a suit that isn't circle
        with self.assertRaises(InvalidCardError):
            w.play(1)

        with self.assertRaises(InvalidCardError):
            w.play(2)
        
        with self.assertRaises(InvalidCardError):
            w.play(3)
        
        with self.assertRaises(InvalidCardError):
            w.play(4)

        result = w.play(0)

        # Check if the engine is in request mode
        self.assertFalse(w.request_mode)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_2")

        self.assertEqual(w.game_state()["current_player"], "player_3")

    # TODO: Fix the initial card bug in the british mode
    def test_nigerian_mode_pick_two_on_game_start(self):

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

        w.Nigerian_Mode = False

        # Start game
        w.start_game()

        # Check if the engine is in pick mode
        self.assertEqual(w.pick_mode, True)

        # Player one goes to market
        w.market()

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 3)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 2)
        self.assertEqual(len(w.game_state()["players"]["player_4"]), 2)

        self.assertEqual(w.game_state()["current_player"], "player_2")
    
    def test_nigerian_mode_suspension_on_game_start(self):
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

        w.Nigerian_Mode = False

        # Start game
        w.start_game()

        # Check that the player two is the current player
        self.assertEqual(w.game_state()["current_player"], "player_1")

    def test_nigerian_mode_go_gen_game_start(self):
        """
        This test checks if the suspension logic works on game start.
        """

        # Define top pile card
        pile = Card(Suit.TRIANGLE, 14)

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

        w.Nigerian_Mode = False

        # Start game
        w.start_game()


        self.assertEqual(len(w.game_state()["players"]["player_1"]), 3)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 3)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 3)

        # Check that the player two is the current player
        self.assertEqual(w.game_state()["current_player"], "player_12")



if __name__ == '__main__':
    unittest.main()
