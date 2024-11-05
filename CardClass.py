# import random
# class Card:
#     def __init__(self, rank, suit, imagePath):
#         self.suit = suit
#         self.rank = rank
#         self.isFaceUp = False
#         self.cardImage = imagePath

#     def flipCard(self):
#         if not self.isFaceUp:
#             self.isFaceUp = True
#             self.cardImage = f"CardImages/{checkRank(self.rank)}_of_{self.suit.lower()}.png"
#         else:
#             self.isFaceUp = False
#             self.cardImage = f"SuitsImages/back.jpeg"

#     def getCardImage(self):
#         if self.isFaceUp:
#             return f"CardImages/{checkRank(self.rank)}_of_{self.suit.lower()}.png"
#         else:
#             return f"SuitsImages/back.jpeg"


# cards = []


# def AddCard(rank, suit, imagePath):
#      cards.append(Card(rank, suit, imagePath))


# def InitializeDeck():
#     ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
#     suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

#     for suit in suits:
#         for rank in ranks:
#             imagePath = f"CardImages/{checkRank(rank)}_of_{suit.lower()}.png"
#             AddCard(checkRank(rank), suit, imagePath)  
    
#     deck = ShuffleCards(cards)
#     return deck


# def ShuffleCards(cards):
#     for i in range(len(cards)):
#         randomIndex = random.randint(0,len(cards)-1)
#         cards[i], cards[randomIndex] = cards[randomIndex], cards[i]
#     return cards
    
# def checkRank(rank):
#     if rank == 'A':
#         return "ace"
#     elif rank == 'J':
#         return "jack"
#     elif rank == 'Q':
#         return "queen"
#     elif rank == 'K':
#         return "king"
#     else:
#         return rank



import random
class Card:
    def __init__(self, rank, suit, imagePath):
        self.suit = suit
        self.rank = rank
        self.isFaceUp = False
        self.cardImage = imagePath

    def flipCard(self):
        if not self.isFaceUp:
            self.isFaceUp = True
            self.cardImage = f"CardImages/{checkRank(self.rank)}_of_{self.suit.lower()}.png"
        else:
            self.isFaceUp = False
            self.cardImage = f"SuitsImages/back.jpeg"

    def getCardImage(self):
        if self.isFaceUp:
            return f"CardImages/{checkRank(self.rank)}_of_{self.suit.lower()}.png"
        else:
            return f"SuitsImages/back.jpeg"

    def getState(self):
        if self.isFaceUp:
            return "Face-Up"
        else:
            return "Face-Down"

    def getCardDetail(self):
        return f"{checkRank(self.rank)}_of_{self.suit.lower()}"


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



        