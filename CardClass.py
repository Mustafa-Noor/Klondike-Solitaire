class Card:
    def __init__(self, rank, suit, imagePath):
        self.suit = suit
        self.rank = rank
        self.isFaceUp = False
        self.cardImage = imagePath

    def flipCard(self):
        if not isFaceUp:
            isFaceUp = True
        else:
            isFaceUp = False




cards = {}


def AddCard(cardID, rank, suit, imagePath):
    cards[cardID] = Card(rank, suit, imagePath)


def InitializeDeck():
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    for suit in suits:
        for rank in ranks:
            cardID = f"{rank}-{suit}"  
            imagePath = f"CardImages/{checkRank(rank)}_of_{suit.lower()}.png"
            print(imagePath)
            AddCard(cardID, rank, suit, imagePath)  
    
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



        