from CardEngine import Rank, Suit, Hand, Deck
from msvcrt import getch, kbhit

games = 0

scores = {
    "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
    "6": 0, "7": 0, "8": 0
}

names = [
    "High Card", "Pair", "Two Pair", "Trips", "Straight", "Flush", "Full House", "Quad", "Straight Flush"
    ]

def main():
    global games
    global scores
    
    deck = Deck()
    player = Hand()

    while True:

        for i in range(5):
            player.addCard(deck.randomCard())

        print(player.handDescription())
        
        scores[str(player.handScore[0])] += 1

        if player.handScore[0] >= 8:
            return

        while not player.isEmpty():
            deck.addCard(player.discard(0))

        games += 1
        waiting = kbhit()
        if waiting:
            key = getch()
            if key == b"\r":
                return

        deck.shuffle()

main()
print(games, "hands")
for i in names:
    print(i, scores[str(names.index(i))])

a = input()

