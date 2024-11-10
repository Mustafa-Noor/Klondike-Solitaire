
class Node:
    def __init__(self, card): # this is the constructor of card node class
        self.card = card
        self.next = None

class LinkedListCards:
    def __init__(self): # constructor of the linked list head is none
        self.head = None


    # this is to add a card in the linked list
    def AddCard(self, card):
        newNode = Node(card)
        if self.head is None:
            self.head = newNode
        else:
            temp = self.head
            while(temp.next != None):
                temp = temp.next    
            temp.next = newNode

    # this is to add multiple cards in the linked list through a node and return its count
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
            
    # this is to return node at an index and end its next reference
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


    # this is to only get a node at index
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
                

    # this is to remove card from the end of the list
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

    # this is to peak card at the end of the list
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

    # this si to get the size of the linked list
    def getSize(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    # this is to check if the linked list is empty or not
    def isEmpty(self):
        return self.head == None
