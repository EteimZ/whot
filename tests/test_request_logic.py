import unittest
from whot import *
from whot.exceptions import InvalidCardError, GameNotStartedError, GameOverError, InvalidSuitError, InvalidMoveError


class TestRequestLogic(unittest.TestCase):

    def test_whot(self):
        """
        Test to see if the whot card can be played at any time.
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
        result = w.play(1)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "request")
        self.assertEqual(result["player_id"], "player_1")


        # Check if the engine is in request mode
        self.assertTrue(w.request_mode)

        self.assertEqual(w.game_state()["current_player"], "player_1")

    def test_request_initial_card(self):
        """
        Test the engine's functionality when the initial card is a whot card
        """

        # Define top pile card
        pile = Card(Suit.WHOT, 20)

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

        # Start game
        w.start_game()

        # Check if the engine is in request mode
        self.assertTrue(w.request_mode)

        # player 1 makes a request
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

    def test_request_circle(self):
        """
        Test to see if a player can request for the circle suit.
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

    def test_request_triangle(self):
        """
        Test to see if a player can request for the triangle suit.
        """

        # Define top pile card
        pile = Card(Suit.STAR, 7)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.TRIANGLE, 13)
        card7 = Card(Suit.CIRCLE, 4)
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
        request_result = w.request("triangle")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "triangle")
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

    def test_request_cross(self):
        """
        Test to see if a player can request for the cross suit.
        """

        # Define top pile card
        pile = Card(Suit.CIRCLE, 3)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CROSS, 11)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.SQUARE, 3)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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
        request_result = w.request("cross")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "cross")
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

    def test_request_square(self):
        """
        Test to see if a player can request for the square suit.
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.SQUARE, 3)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.STAR, 4)
        card9 = Card(Suit.CROSS, 11)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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
        request_result = w.request("square")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "square")
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

    def test_request_star(self):
        """
        Test to see if a player can request for the star suit.
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.STAR, 4)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.CROSS, 11)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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
        request_result = w.request("star")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "star")
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

    def test_request_none(self):
        """
        Test that the player can still play a card if other players don't have the requested card.
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 4)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.TRIANGLE, 4)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.CROSS, 11)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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
        request_result = w.request("star")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "star")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")

        # player 2 goes to market
        w.market()

        # player 3 goes to market
        w.market()

        # Player 1 tries to play card suit they didn't request for
        with self.assertRaises(InvalidCardError):
            w.play(1)
        
        with self.assertRaises(InvalidCardError):
            w.play(2)
        
        with self.assertRaises(InvalidCardError):
            w.play(3)

        # plays their actual card suit
        result = w.play(0)

        # Check if the engine is in request mode
        self.assertFalse(w.request_mode)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")

        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_request_whot(self):
        """
        Test that the player can still play a whot card if other players don't have the requested card.
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 4)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.WHOT, 20)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.TRIANGLE, 4)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.CROSS, 11)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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
        request_result = w.request("star")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "star")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")

        # player 2 goes to market
        w.market()

        # player 3 goes to market
        w.market()


        # plays their actual card suit
        result = w.play(1)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "request")
        self.assertEqual(result["player_id"], "player_1")

        # Check if the engine is in request mode
        self.assertTrue(w.request_mode)

    def test_request_invalid_suit(self):
        """
        Test to see if a player can request for the circle suit.
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
        
        # Check if engine raises an error if the player requests for a whot card
        with self.assertRaises(InvalidSuitError):
            w.request("whot")

        # Check if engine raises an error if the player requests for a suit that doesn't exist
        with self.assertRaises(InvalidSuitError):
            w.request("what")

        self.assertEqual(w.game_state()["current_player"], "player_1")


    def test_request_game_not_started(self):
        """
        Test that request's can't be made if the game hasn't started
        """

        # Define top pile card
        pile = Card(Suit.WHOT, 20)

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

        # player makes a request when the game hasn't started
        with self.assertRaises(GameNotStartedError):
            w.request("circle")

    def test_request_game_over(self):
        """
        Test the engine's functionality when the initial card is a whot card
        """

        # Define top pile card
        pile = Card(Suit.STAR, 7)

        # Define player cards
        card1 = Card(Suit.WHOT, 20)

        card2 = Card(Suit.CIRCLE, 4)

        card3 = Card(Suit.TRIANGLE, 5)

        # Create players
        test_players = [[card1], [card2], [card3]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        # Start game
        w.start_game()

        # Player one plays the pick two card
        result = w.play(0)

        # Assert results
        self.assertFalse(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_1")        
        
        # Check if a game over error is raised 
        with self.assertRaises(GameOverError):
            w.request("circle")

    def test_request_mode(self):
        """
        Test to see if a player can request for the triangle suit.
        """

        # Define top pile card
        pile = Card(Suit.STAR, 7)

        # Define player cards
        card1 = Card(Suit.TRIANGLE, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.TRIANGLE, 13)
        card7 = Card(Suit.CIRCLE, 4)
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

        # Start game
        w.start_game()

        # request for a card before playing the whot card
        with self.assertRaises(InvalidMoveError):
            w.request("triangle")

        self.assertEqual(w.game_state()["current_player"], "player_1")


class TestRequestLogicSpecialCards(unittest.TestCase):
    
    def test_request_hold_on(self):
        """
        Test the hold on logic in the request mode
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.STAR, 1)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.CROSS, 11)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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

        # request for suit 
        request_result = w.request("star")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "star")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")

        result = w.play(0)

        self.assertFalse(w.request_mode)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "hold_on")
        self.assertEqual(result["player_id"], "player_2")

        self.assertEqual(w.game_state()["current_player"], "player_2")

    def test_request_pick_two(self):
        """
        Test the pick two logic in the request mode
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CIRCLE, 2)
        card7 = Card(Suit.STAR, 1)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.CROSS, 11)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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

        # request for suit 
        request_result = w.request("circle")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "circle")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")

        result = w.play(0)

        self.assertFalse(w.request_mode)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "pick_2")
        self.assertEqual(result["player_id"], "player_2")

        self.assertEqual(w.game_state()["current_player"], "player_3")

        w.market()

        self.assertEqual(len(w.game_state()["players"]["player_3"]), 7)

    def test_request_pick_two_defence(self):
        """
        Test the pick two defence logic works in the request mode
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 3)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CIRCLE, 2)
        card7 = Card(Suit.STAR, 1)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.CROSS, 11)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.STAR, 2)
        card12 = Card(Suit.TRIANGLE, 5)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

        # Start game
        w.start_game()

        # Player one plays the pick two card
        result = w.play(1)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "request")
        self.assertEqual(result["player_id"], "player_1")


        # Check if the engine is in request mode
        self.assertEqual(w.request_mode, True)

        # Check the current player is still player one despite playing the whot card
        self.assertEqual(w.game_state()["current_player"], "player_1")

        # request for suit 
        request_result = w.request("circle")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "circle")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")

        result = w.play(0)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "pick_2")
        self.assertEqual(result["player_id"], "player_2")

        self.assertEqual(w.game_state()["current_player"], "player_3")

        result = w.play(0)

        self.assertFalse(w.request_mode)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_3")


        self.assertEqual(len(w.game_state()["players"]["player_3"]), 4)

        w.market()

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 8)

    def test_request_pick_three(self):
        pass

    def test_request_suspension(self):
        """
        Test suspension logic in request mode
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.STAR, 8)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.CROSS, 11)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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

        # request for suit 
        request_result = w.request("star")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "star")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")

        result = w.play(0)

        self.assertFalse(w.request_mode)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "suspension")
        self.assertEqual(result["player_id"], "player_2")

        self.assertEqual(w.game_state()["current_player"], "player_1")

    def test_request_go_gen(self):
        """
        Test suspension logic in request mode
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.CROSS, 14)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.STAR, 8)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.TRIANGLE, 5)
        card12 = Card(Suit.STAR, 3)
        card13 = Card(Suit.CROSS, 13)
        card14 = Card(Suit.CIRCLE, 10)
        card15 = Card(Suit.SQUARE, 7)


        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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

        # request for suit 
        request_result = w.request("cross")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "cross")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")

        result = w.play(0)

        self.assertFalse(w.request_mode)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "general_market")
        self.assertEqual(result["player_id"], "player_2")

        # self.assertEqual(w.game_state()["current_player"], "player_2")

        self.assertEqual(len(w.game_state()["players"]["player_1"]), 5)
        self.assertEqual(len(w.game_state()["players"]["player_2"]), 4)
        self.assertEqual(len(w.game_state()["players"]["player_3"]), 6)

    def test_request_whot_double(self):
        """
        Test if the second player can change the requested suit using their own whot card
        """

        # Define top pile card
        pile = Card(Suit.SQUARE, 11)

        # Define player cards
        card1 = Card(Suit.STAR, 2)
        card2 = Card(Suit.WHOT, 20)
        card3 = Card(Suit.CROSS, 2)
        card4 = Card(Suit.SQUARE, 14)
        card5 = Card(Suit.CIRCLE, 1)

        card6 = Card(Suit.WHOT, 20)
        card7 = Card(Suit.CIRCLE, 4)
        card8 = Card(Suit.SQUARE, 3)
        card9 = Card(Suit.STAR, 8)
        card10 = Card(Suit.TRIANGLE, 13)

        card11 = Card(Suit.CROSS, 13)
        card12 = Card(Suit.CIRCLE, 10)
        card13 = Card(Suit.TRIANGLE, 5)
        card14 = Card(Suit.STAR, 3)
        card15 = Card(Suit.SQUARE, 7)

        # Create players
        test_players = [[card1, card2, card3, card4, card5], [card6, card7, card8, card9, card10], [card11, card12, card13, card14, card15]]

        # Initialize test engine
        w = TestWhot(pile, test_players)

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

        # request for suit 
        request_result = w.request("cross")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "cross")
        self.assertEqual(request_result["player_id"], "player_1")

        # Confirm that is the next players turn
        self.assertEqual(w.game_state()["current_player"], "player_2")

        result = w.play(0)

        # Assert results
        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "request")
        self.assertEqual(result["player_id"], "player_2")


        # Check if the engine is in request mode
        self.assertTrue(w.request_mode)

        # Check the current player is still player one despite playing the whot card
        self.assertEqual(w.game_state()["current_player"], "player_2")

        # request for suit 
        request_result = w.request("circle")

        # Confirm request result
        self.assertEqual(request_result["requested_suit"], "circle")
        self.assertEqual(request_result["player_id"], "player_2")


        with self.assertRaises(InvalidCardError):
            w.play(0)

        result = w.play(1)

        self.assertTrue(result["status"])
        self.assertEqual(result["type"], "normal")
        self.assertEqual(result["player_id"], "player_3")

        self.assertEqual(w.game_state()["current_player"], "player_1")


if __name__ == '__main__':
    unittest.main()