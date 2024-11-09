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
            "spades" : [],
            "clubs" : [],
            "hearts" : [],
            "diamonds" : []
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

    def AddtoTableauDict(self, column, card):
        if column in self.tableau:
            self.tableau[column].append(card)
            self.cardState[card.getCardDetail()] = card.getState()
    
    def RemoveFromTableauDict(self, column, card): 
        if column in self.tableau: 
            if card in self.tableau[column]: 
                self.tableau[column].remove(card) 
                del self.cardState[card.getCardDetail()] 
                if not self.tableau[column]: 
                    del self.tableau[column]


    def AddToFoundationDict(self, suit, card):
        self.foundationPiles[suit.lower()].append(card)
