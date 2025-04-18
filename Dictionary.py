class Dictionaries:
    def __init__(self):

        # this is to keep track of the cards in the colummns
        self.tableau = {
            "column1" : [],
            "column2" : [],
            "column3" : [],
            "column4" : [],
            "column5" : [],
            "column6" : [],
            "column7" : []
        }

        # this is to keep traack of the card in the foundation piles
        self.foundationPiles = {
            "spadespile" : [],
            "clubspile" : [],
            "heartspile" : [],
            "diamondspile" : []
        }

        # this is to keep track of the card states on the basis of their details
        self.cardState = {}


        # this mapping is used for validation of movement
        self.colourMap = {
            'hearts': 'red',
            'diamonds': 'red',
            'spades' : 'black',
            'clubs' : 'black'
        }

        # this mappping is also used for validation of movement
        self.rankMap = {
            'ace' : 1,
            'jack' : 11,
            'queen' : 12,
            'king' : 13
        }

    # this is used to return the rank to int based on dictionary
    def getRank(self, rank):
        if rank.lower() in self.rankMap:
            return self.rankMap[rank.lower()]
        else:
            return int(rank)

    # this is to return entire tableau
    def getTableau(self):
        return self.tableau

    # this is to change the state of the card
    def changeState(self, card, faceUp):
        cardDetails = card.getCardDetail()
        if cardDetails not in self.cardState:
            self.AddCardToStates(card)
        card.isFaceUp = faceUp
        self.cardState[cardDetails] = card.getState()

# this is to add a card with its details in the state dictionary
    def AddCardToStates(self, card):
        self.cardState[card.getCardDetail()] = card.getState()

    # this is to add a card in the tableau dict
    def AddtoTableauDict(self, column, card):
        if column in self.tableau:
            self.tableau[column].append(card)
            self.cardState[card.getCardDetail()] = card.getState()
    
    # this is to remove a card from tableau
    def RemoveFromTableauDict(self, column, card): 
        if column in self.tableau: 
            if card in self.tableau[column]: 
                self.tableau[column].remove(card) 
                del self.cardState[card.getCardDetail()] 

    # these are for adding or removing cards from foundation dictionary

    def AddToFoundationDict(self, suit, card):
        self.foundationPiles[suit.lower()].append(card)

    def RemoveFromFoundationDict(self, suit, card):
        if suit.lower() in self.foundationPiles:
            if card in self.foundationPiles[suit.lower()]:
                self.foundationPiles[suit.lower()].remove(card)

    # this displays all of the dictionaries
    def DisplayAllDictionary(self):
        print()
        print("Foundation Piles")
        for pile, cards in self.foundationPiles.items():
            print(f"Pile: {pile}")
            for card in cards:
                print(f"Card: {card.getCardDetail()}")

        print("\nCard States:") 
        for cardDetails, state in self.cardState.items():
             print(f"Card: {cardDetails}, State: {state}")


    # this gives the state of the card
    def giveState(self, card):
        if card.getCardDetail() in self.cardState:
            return self.cardState[card.getCardDetail()]
        else:
            return None

