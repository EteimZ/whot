from whot import Whot, Player, Deck, Card, Suit

p1 = Player("Eteims")
p2 = Player("Jacob")
p3 = Player("Ted")

d = Deck()
d.shuffle()
# print(d.cards)

p1.recieve(d.deal_card(4))

g = Whot(4)
print(g.game_state())
g.play(Card(Suit.ANGLE, 1))
