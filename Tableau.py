class Node:
    def __init__(self, card):
        self.card = card
        self.next = None
        
    def getCard(self):
        return self.card

class TableauPile:
    def __init__(self):
        self.head = None
        self.top = None  # This will point to the top of the stack

    def push(self, card):
        new_node = Node(card)
        if self.head is None:
            self.head = new_node
            self.top = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def isEmpty(self):
        return self.head is None

    def pop(self):
        if not self.isEmpty():
            card = self.head.card
            self.head = self.head.next  
            if self.head is None:  
                self.top = None
            return card
        return None

    def checkNext(self):
        return self.getSize() == 1

    def getSize(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
