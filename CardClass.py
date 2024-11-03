import random
class Card:
    def __init__(self, rank, suit, imagePath):
        self.suit = suit
        self.rank = rank
        self.isFaceUp = False
        self.cardImage = imagePath

    def flipCard(self):
        if not isFaceUp:
            isFaceUp = True
            imagePath = f"CardImages/{sef.checkRank(rank)}_of_{self.suit.lower()}.png"
        else:
            isFaceUp = False
            imagePath = f"SuitsImages/back.jpeg"



cards = []


def AddCard(rank, suit, imagePath):
     cards.append(Card(rank, suit, imagePath))


def InitializeDeck():
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    for suit in suits:
        for rank in ranks:
            imagePath = f"CardImages/{checkRank(rank)}_of_{suit.lower()}.png"
            AddCard(checkRank(rank), suit, imagePath)  
    
    random.shuffle(cards)
    return cards


def ShuffleCards(cards):
    random.shuffle(cards)
    return cards
    
def checkRank(rank):
    if rank == 'A':
        return "ace"
    elif rank == 'J':
        return "jack"
    elif rank == 'Q':
        return "queen"
    elif rank == 'K':
        return "king"
    else:
        return rank



        