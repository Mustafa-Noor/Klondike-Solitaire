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
        else:
            temp = self.head
            while(temp.next != None):
                temp = temp.next    
            temp.next = newNode
            

    def removeCardFromLast(self):
        if self.head is None:
            return None
        
        if self.head.next is None:
            removedCard = self.head.card
            self.head = None  
            return removedCard

        temp = self.head
        while(temp.next.next != None):
            temp = temp.next
        
        removedCard = temp.next.card
        temp.next = None
        return removedCard

    def peakLast(self):
        if self.head is None:
            return None
        
        if self.head.next is None:
            removedCard = self.head.card
            return removedCard

        temp = self.head
        while(temp.next.next != None):
            temp = temp.next
        
        removedCard = temp.next.card
        return removedCard

    
    def getSize(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def isEmpty(self):
        return self.head == None
