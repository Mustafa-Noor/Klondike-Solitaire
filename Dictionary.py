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


    def getTableau(self):
        return self.tableau

    def AddtoTableauDict(self, column, card):
        if column in self.tableau:
            self.tableau[column].append(card)
            self.cardState[card.getCardDetail()] = card.getState()
    
    def AddToFoundationDict(self, suit, card):
        self.foundationPiles[suit.lower()].append(card)
