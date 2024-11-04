class CardNode:
    def __init__(self, card):
        self.card = card
        self.next = None
    
class TableauPile:
    def __init__(self):
        self.head = None
    

    def push(self, card):
        newNode = CardNode(card)
        if(self.head == None):
            self.head = newNode
        else:
            temp = self.head
            newNode.next = temp
            self.head = newNode

    def pop(self):
        if(self.head == None):
            print("Pile is empty!!!")
            return
        else:
            temp = self.head.card
            self.head = self.head.next
            return temp

    def peek(self):
        if self.head is None:
            return None

        return self.head.card

    def getSize(self):
        size = 0
        temp = self.head
        while temp is not None:  # Check for None instead of temp.next
            size += 1
            temp = temp.next
        return size

    def is_valid_move(self, card):
        """Check if moving 'card' onto this tableau pile follows Solitaire rules."""
        # If the tableau is empty, only kings (rank 13) can be placed here
        if not self.cards:
            return card.rank == 13  # Assuming rank 13 represents a King

        top_card = self.peek()

        # Check descending order and alternating colors
        return (
            card.rank == top_card.rank - 1 and
            card.color != top_card.color
        )

    def isEmpty(self):
        if self.head is None:
            return True

        return False