from colorama import Fore, Back, Style, init
import os

from CardEngine import Rank, Suit, Card, Hand, Deck
from KBIO import numberInput

init()

def showHand(hand):
    print(hand.toString() + ("   " * (hand.handSize - len(hand.hand))), end="\r")

def main():
    the_deck = Deck()
    player = Hand()
    games = 0
    while True:
        try:
            games += 1

            for i in range(5):
                player.addCard(the_deck.randomCard())

            print("Game #", games)
            print("".join(" " + str(i + 1) + " " for i in range(player.handSize)))
            showHand(player)
            
            discard = []
            while True:

                index = numberInput(mi = 1, ma = player.handSize)
                
                if index >= 1 and index <= player.handSize:
                    discard.append(player.discard(index - 1))
                    showHand(player)
                elif index == -1:
                    break
                else:
                    continue

            for i in range(len(discard)):
                player.addCard(the_deck.randomCard())
                the_deck.addCard(discard[i])

            showHand(player)

            print("\n" + player.handDescription())

            a = input("Paused...\nPress enter to continue")

            while not player.isEmpty():
                the_deck.addCard(player.discard(0))

            os.system("cls")
            the_deck.shuffle()
        except Exception as e:
            print(e)
            
if __name__ == "__main__":
    main()
    a = input()
