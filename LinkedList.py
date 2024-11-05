class Node:
    def __init__(self, card):
        self.card = card
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self.head = None
    