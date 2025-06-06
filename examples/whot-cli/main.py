from whot import Whot

g = Whot(2, number_of_cards=2)
g.start_game()

cards = ["circle", "square", "star", "cross", "triangle"]

while True:
    print(g.game_state())
  
    print("1. Play")
    print("2. Market")
    print("3. Exit")
    option = int(input("Select option: "))
    
    if option == 1:
        n = int(input("Provide card index: "))

        result = g.play(n)
        if result["status"] == True:
            if result["type"] == "request":
                print("0. Circle")
                print("1. Square")
                print("2. Star")
                print("3. Cross")
                print("4. Angle")
                suit = int(input("Provide suit: "))
                print(cards[suit])
                request_card = g.request(cards[suit])
                print(f"I need: {request_card}")
            
        else:
            print(f"Player: {result['player_id']} wins!")
            break

    elif option == 2:
        g.market()
    elif option == 3:
        break
    else:
        print("Unknown option")