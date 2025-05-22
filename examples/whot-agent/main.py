from whot import Whot
from whot.agent import Agent

g = Whot(2, number_of_cards=2)
a = Agent("player_2", g)
g.start_game()

cards = ["circle", "square", "star", "cross", "triangle"]

while True:
    print(g.game_state())
    
    if g.game_state()["current_player"] == a.agent_id:
        a.play()

    else:
        print("1. Play")
        print("2. Market")
        print("3. Exit")
        option = int(input("Select option: "))
        
        if option == 1:
            n = int(input("Provide card index: "))
            result = g.play(n)
            print(result)
            if result["status"] == "GameOver":
                print(f"Human wins!")
                break

            if result["status"] == "Request":
                print("0. Circle")
                print("1. Square")
                print("2. Star")
                print("3. Cross")
                print("4. Angle")
                suit = int(input("Provide suit: "))
                print(cards[suit])
                request_card = g.request(cards[suit])
                print(f"I need: {request_card}")

        elif option == 2:
            g.market()
        elif option == 3:
            break
        else:
            print("Unknown option")