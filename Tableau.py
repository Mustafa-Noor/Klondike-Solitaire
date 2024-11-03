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
        while(temp.next):
            size += 1
            temp = temp.next
        return size

    def isEmpty(self):
        if self.head is None:
            return True

        return False