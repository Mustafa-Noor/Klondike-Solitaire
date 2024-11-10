class Dictionaries:
    def __init__(self):

        self.tableau = {
            "column1" : [],
            "column2" : [],
            "column3" : [],
            "column4" : [],
            "column5" : [],
            "column6" : [],
            "column7" : []
        }

        self.foundationPiles = {
            "spadespile" : [],
            "clubspile" : [],
            "heartspile" : [],
            "diamondspile" : []
        }

        self.cardState = {}


        self.colourMap = {
            'hearts': 'red',
            'diamonds': 'red',
            'spades' : 'black',
            'clubs' : 'black'
        }

    def getTableau(self):
        return self.tableau

    def changeState(self, card, faceUp):
        cardDetails = card.getCardDetail()
        if cardDetails not in self.cardState:
            self.AddCardToStates(card)
        card.isFaceUp = faceUp
        self.cardState[cardDetails] = card.getState()


    def AddCardToStates(self, card):
        self.cardState[card.getCardDetail()] = card.getState()

    def AddtoTableauDict(self, column, card):
        if column in self.tableau:
            self.tableau[column].append(card)
            self.cardState[card.getCardDetail()] = card.getState()
    
    def RemoveFromTableauDict(self, column, card): 
        if column in self.tableau: 
            if card in self.tableau[column]: 
                self.tableau[column].remove(card) 
                del self.cardState[card.getCardDetail()] 

    def AddToFoundationDict(self, suit, card):
        self.foundationPiles[suit.lower()].append(card)

    def RemoveFromFoundationDict(self, suit, card):
        if suit.lower() in self.foundationPiles:
            if card in self.foundationPiles[suit.lower()]:
                self.foundationPiles[suit.lower()].remove(card)


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
             

    def giveState(self, card):
        if card.getCardDetail() in self.cardState:
            return self.cardState[card.getCardDetail()]
        else:
            return None

