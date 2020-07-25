try:
    from colorama import Fore, Back, Style
    COLOR = True
except ImportError:
    COLOR = False

import random
import itertools

class HandFullError(Exception):
    pass

class Rank():

    ranks = [
        "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"
        ]

    def __init__(self, value):
        try:
            self.value = int(value)
        except:
            value = value.upper()
            self.value = Rank.ranks.index(value) + 2

    def toString(self):
        return Rank.ranks[self.value - 2]

    def toValue(self):
        return self.value

class Suit():

    suits = [
        "h", "s", "d", "c"
        ]

    def __init__(self, value):
        try:
            self.value = int(value)
        except:
            value = value.lower()
            self.value = Suit.suits.index(value) + 1
        finally:
            if self.value == 1 or self.value == 3:
                self.color = "red"
            else:
                self.color = "black"

    def toString(self):
        return Suit.suits[self.value - 1]
    
    def toValue(self):
        return self.value

class Card():

    def __init__(self, rank=Rank("A"), suit=Suit("h")):
        if type(rank) is str or type(rank) is int:
            self.rank = Rank(rank)
        else:
            self.rank = rank

        if type(suit) is str:
            self.suit  = Suit(suit)
        else:
            self.suit = suit

    def toString(self, color=True):
        global COLOR
        returnStr = self.rank.toString() + self.suit.toString()
        if COLOR and color:
            returnStr = Back.WHITE + returnStr + Style.RESET_ALL
            if self.suit.color == "red":
                return Fore.RED + Style.BRIGHT + returnStr
            elif self.suit.color == "black":
                return Fore.BLACK + returnStr
        else:    
            return returnStr

    def compare(self, card):
        "True if self larger than card passed"
        return self.rank.toValue() > card.rank.toValue()

    def parseStr(string):
        newCard = Card()
        if string[0] in Rank.ranks:
            newCard.rank = Rank(string[0])

class Hand():

    def __init__(self, *args, handSize=5):
        self.handSize = handSize
        self.hand = []
        for arg in args:
            if type(arg) is list:
                if len(arg) <= 2:
                    self.addCard(Card(arg[0], arg[1]))
            elif type(arg) is tuple and len(arg) == self.handSize:
                self.hand = list(arg)
            elif type(arg) is Card:
                self.addCard(arg)
                    
    def isEmpty(self):
        return len(self.hand) == 0

    def isFull(self):
        return len(self.hand) == self.handSize

    def toString(self, color=True):
        if not self.isEmpty():
            handString = [card.toString(color=color) for card in self.hand]
            return " ".join(handString)
        else:
            return ""

    def addCard(self, card):
        if not self.isFull():
            self.hand.append(card)

    def discard(self, index):
        if not self.isEmpty():
            return self.hand.pop(index)
        else:
            return None

    def handDescription(self):
        handScore = Hand.scoreHand(self)
        self.handScore = handScore
        return Hand.scoreString(self.handScore)

    def scoreString(handScore):
        if handScore[0] == 8:
            if handScore[1] == 13:
                return "Royal Flush"
            else:
                if handScore[2][1] == 5 and handScore[2][0] == 14:
                    value = 1
                else:
                    value = 0
                return "Straight Flush, " + Rank(handScore[2][value]).toString() + " high"
                
        elif handScore[0] == 7:
            return "Quad " + Rank(handScore[1]).toString() + "s"
        elif handScore[0] == 6:
            return "Full House, " + Rank(handScore[1][0]).toString() + "s full of " + Rank(handScore[2][0]).toString() + "s"
        elif handScore[0] == 5:
            return "Flush, " + " ".join( [Rank(i).toString() for i in handScore[1] ] )
        elif handScore[0] == 4:
            if handScore[2][1] == 5 and handScore[2][0] == 14:
                value = 1
            else:
                value = 0
            return "Straight, " + Rank(handScore[2][value]).toString() + " high"
        elif handScore[0] == 3:
            return "Three of a Kind " + Rank(handScore[1][0]).toString() + "s"
        elif handScore[0] == 2:
            return "Two Pair " + Rank(handScore[1][0]).toString() + "s and " + Rank(handScore[1][1]).toString() + "s"
        elif handScore[0] == 1:
            return "Pair of " + Rank(handScore[1][0]).toString() + "s"
        elif handScore[0] == 0:
            return "High Card " + Rank(max(handScore[2])).toString()
        else:
            return "Error in calculation"

    def scoreHand(hand): # Returns (Score, Kicker, Hand Values)
        values = sorted([card.rank.value for card in hand.hand], reverse=True)
        suits = [card.suit.value for card in hand.hand]

        straight = (values == list(range(values[0], values[0] -5, -1))
                    or values == [14, 5, 4, 3, 2])
        
        flush = all(suit == suits[0] for suit in suits)
        
        if straight and flush:
            return 8, values[1], values # Straight / Royal Flush
        if flush:
            return 5, values    # Flush
        if straight:
            return 4, values[1], values # Straight

        trips = []
        pairs = []
        for v, group in itertools.groupby(values):
            count = sum(1 for i in group)
            if count == 4:
                return 7, v, values # Quads
            elif count == 3:
                trips.append(v)
            elif count == 2:
                pairs.append(v)

        if trips:
            return (6 if pairs else 3), trips, pairs, values # Full House / Trips

        return len(pairs), pairs, values # Two Pair / One Pair / High Card

    def compareHands(hand1, hand2):

        hand1Score = Hand.scoreHand(hand1)
        hand2Score = Hand.scoreHand(hand2)
        if hand1Score > hand2Score:
            return hand1
        elif hand2Score > hand1Score:
            return hand2
        else:
            return -1

    def score7(hand): # Score a hand of seven cards (e.g. holdem)
        if len(hand.hand) != 7:
            raise ValueError
        else:
            combinations = itertools.combinations(hand.hand, 5)
            maxScore = ()
            
            for combination in combinations:
                comboHand = Hand(combination)
                score = Hand.scoreHand(comboHand)
                if score >= maxScore:
                    maxScore = score

            return maxScore


class Deck():

    standardDeck = [
        Card(rank=Rank(i), suit=Suit(j)) for i in range(2, 15) for j in range(4)
        ]

    def __init__(self):
        self.deck = Deck.standardDeck.copy()
        self.deckSize = len(self.deck)
        random.shuffle(self.deck)

    def randomCard(self):
        if not self.isEmpty():
            card = self.deck[0]
            del self.deck[0]
            self.deckSize -= 1
            return card

    def peek(self):
        return self.deck[0]

    def addCard(self, card):
        if not self.isFull():
            self.deck.append(card)
            self.deckSize += 1

    def isFull(self):
        return self.deckSize == len(Deck.standardDeck)

    def isEmpty(self):
        return self.deckSize == 0

    def shuffle(self):
        random.shuffle(self.deck)
