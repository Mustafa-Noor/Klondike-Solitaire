class Node:
    def __init__(self, card):
        self.card = card
        self.next = None
        self.prev = None

class LinkedListCards:
    def __init__(self):
        self.head = None


    def AddCard(self, card):
        newNode = Node(card)
        if self.head is None:
            self.head = newNode
            return

        temp = self.head
        while(temp.next != None):
            temp = temp.next    

        temp.next = newNode
    
    def getSize(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    