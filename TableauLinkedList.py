from Card import Card  
from Card import cards

class Node:
    def __init__(self, card):
        self.card = card
        self.next = None

class TableauPile:
    def __init__(self):
        self.head = None

    def AddCardInPile(self, card):
        newNode = Node(card)
        newNode.next = self.head
        self.head = newNode

    def RemoveCard(self):
        if self.head is None:
            return None
        cardToRemove = self.head.card
        self.head = self.head.next
        return cardToRemove


    def PeekTopCard(self):
        if self.head is None:
            return None
        return self.head.card

    def DisplayPile(self):
        current = self.head
        while current:
            print(current.card)
            current = current.next

tableau_pile = TableauPile()
tableau_pile.AddCardInPile(cards['A-Hearts'])  # Adding 'A-Hearts' to the tableau pile
tableau_pile.AddCardInPile(cards['2-Spades'])  # Adding '2-Spades' to the tableau pile

print("Top card in tableau:")
print(tableau_pile.PeekTopCard())  # Should print '2-Spades'

tableau_pile.RemoveCard()  # Remove the top card ('2-Spades')