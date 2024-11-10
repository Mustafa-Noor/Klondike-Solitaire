
import random
class Card: 
    def __init__(self, rank, suit, imagePath): # this is the constructor of the card class which takes its attributes
        self.suit = suit
        self.rank = rank
        self.isFaceUp = False
        self.cardImage = imagePath

    # this is used to flip the state of the card
    def flipCard(self):
        if not self.isFaceUp:
            self.isFaceUp = True
        else:
            self.isFaceUp = False
            
    # this return the card image based on if its face up or not
    def getCardImage(self):
        if self.isFaceUp is True:
            return f"CardImages/{checkRank(self.rank)}_of_{self.suit.lower()}.png"
        else:
            return f"SuitsImages/back.jpeg"

    # this returns the state of the card
    def getState(self):
        if self.isFaceUp:
            return "Face-Up"
        else:
            return "Face-Down"

    # this return the detail of the card
    def getCardDetail(self):
        return f"{checkRank(self.rank)}_of_{self.suit.lower()}"


cards = []
# this is the list of all the 52 cards

# this is to add card in the list of cards
def AddCard(rank, suit, imagePath):
     cards.append(Card(rank, suit, imagePath))

# this is to add cards in the list 
def InitializeDeck():
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    for suit in suits:
        for rank in ranks:
            imagePath = f"CardImages/{checkRank(rank)}_of_{suit.lower()}.png"
            AddCard(checkRank(rank), suit, imagePath)  
    # shuffle the cards
    random.shuffle(cards)
    return cards

# this is used to shuffle the deck
def ShuffleCards(cards):
    random.shuffle(cards)
    return cards
    
# this is used to identify thr rank
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



        