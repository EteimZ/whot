from whot import Game, Player, Deck

p1 = Player("Eteims")
p2 = Player("Jacob")
p3 = Player("Ted")

d = Deck()
g = Game(d, [p1, p2, p3])
g.play()
