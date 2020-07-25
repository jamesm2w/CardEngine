from colorama import Fore, Back, init, Style
import os

from CardEngine import Suit, Rank, Card, Hand, Deck
from msvcrt import kbhit, getch
init()

def showHand(hand):
    print(hand.toString() + ("   " * (hand.handSize - len(hand.hand))))

def showBlankedHand(hand):
    print((Back.WHITE + "  " + Style.RESET_ALL + " ") * hand.handSize)

def showCommunity(com):
    print("Community\t", end="")
    for card in com:
        if card == None:
            print(Back.WHITE + "  " + Style.RESET_ALL + " ", end="")
        else:
            print(card.toString() + " ", end="")

    print(end="\r")

def waitForEnter():
    while True:
        if kbhit():
            if getch() == b"\r":
                return

def main():
    the_deck = Deck()

    player1 = Hand(handSize = 2)
    player2 = Hand(handSize = 2)
    community = [None, None, None, None, None]
    burn = []

    games = 0

    while True:
        try:
            games += 1

            for i in range(2):
                player1.addCard(the_deck.randomCard())
                player2.addCard(the_deck.randomCard())
                
            print("Game", games)
            community = [None, None, None, None, None]
            print("You (P1)\t", end="")
            showHand(player1)
            print()
            print("Player 2\t", end="")
            showBlankedHand(player2)
            print()

            for i in range(3):
                community[i] = the_deck.randomCard()

            showCommunity(community)
            
            for i in range(2):
                waitForEnter()
                burn.append(the_deck.randomCard())
                community[3+i] = the_deck.randomCard()
                showCommunity(community)

            waitForEnter()
            
            print()
            player1Score = Hand.score7(Hand(*(player1.hand + community), handSize=7))
            player2Score = Hand.score7(Hand(*(player2.hand + community), handSize=7))
            print(player1Score)
            print("You (P1) Score:", Hand.scoreString(player1Score))
            print("Player 2 Score:", Hand.scoreString(player2Score))

            if player1Score > player2Score:
                print("Player 1 wins")
            elif player2Score > player1Score:
                print("Player 2 wins")
            else:
                print("Draw")

            waitForEnter()

            for card in community:
                the_deck.addCard(card)

            for card in burn:
                the_deck.addCard(card)

            while not player1.isEmpty():
                the_deck.addCard(player1.discard(0))
            while not player2.isEmpty():
                the_deck.addCard(player2.discard(0))

            #os.system("cls")
            the_deck.shuffle()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
    a = input()

        

        
