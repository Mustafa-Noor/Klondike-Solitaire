class Node:
    def __init__(self, card):
        self.card = card
        self.next = None

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

    def AddCards(self, node):
        count = 0
        if self.head is None:
            self.head = node
        else:
            temp = self.head
            while(temp.next != None):
                temp = temp.next 
                count += 1   
            temp.next = node
        count += 1
        return count
            

    def returnNodeAtIndex(self, index):
        if self.head is None:
            return None

        current = self.head
        prev = None
        
        for i in range(index):
            prev = current
            current = current.next
            if current is None:
                return None
        
        if prev is None:
            self.head = None
        else:
            prev.next = None
        
        return current


    def peakNodeAtIndex(self, index):
        if self.head is None:
            return None

        temp = self.head
        count = 0
        while(count != index and temp is not None):
            temp = temp.next
            count += 1
        if temp is None:
            print("index out of bounds")
            return None
        else:
            nodeToReturn = temp
            return nodeToReturn
                

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
