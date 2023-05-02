from enum import Enum
from dataclasses import dataclass

class Suit(Enum):
    CIRCLE = 0
    SQUARE = 1
    STAR = 2
    CROSS = 3
    ANGLE = 4
    WHOT = 5

''' Cards (Source Wikipedia)
Circles 	1 	2 	3 	4 	5 	  	7 	8 	  	10 	11 	12 	13 	14
Triangles 	1 	2 	3 	4 	5 	  	7 	8 	  	10 	11 	12 	13 	14
Crosses 	1 	2 	3 		5 	  	7 	  	  	10 	11 	  	13 	14
Squares 	1 	2 	3 		5 	  	7 	  		10 	11 	  	13 	14
Stars 	    1 	2 	3 	4 	5 	  	7 	8 	  	  	  	  	  	
5 "Whot" cards numbered 20     
'''
@dataclass
class Card:
    suit: Suit
    value: int

circles = [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14]
triangles = [ 1, 2, 3, 4, 5 , 7, 8, 10, 11, 12, 13, 14 ]
crosses = [ 1, 2, 3, 5, 7, 10, 11, 13, 14]
squares = [ 1, 2, 3, 5, 7, 10, 11, 13, 14]
stars =   [ 1, 2, 3, 4, 5, 7, 8]

cards = []

for circle in circles:
    cards.append(Card(Suit.CIRCLE, circle))


for angle in triangles:
    cards.append(Card(Suit.ANGLE, angle))

for cross in crosses:
    cards.append(Card(Suit.CROSS, cross))

for square in squares:
    cards.append(Card(Suit.SQUARE, square))

for star in stars:
    cards.append(Card(Suit.STAR, star))

for whot in range(5):
    cards.append(Card(Suit.WHOT, whot))

print(cards)
print(len(cards))
