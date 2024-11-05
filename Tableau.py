class Node:
    def __init__(self, card):
        self.card = card
        self.next = None

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
            self.head = self.head.next  # Move the head pointer to the next node
            if self.head is None:  # If the stack is now empty, reset top
                self.top = None
            return card
        return None

    def checkNext(self):
        return self.getSize() is 0  # If head is None, return True

    def getSize(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
