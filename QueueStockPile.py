class QueueNode:
    def __init__(self, card):
        self.card = card
        self.next = None

class StockPileQueue:
    def __init__(self):
        self.front = None
        self.rear = None
    
    def isEmpty(self):
        return self.front is None
    
    def enqueue(self,card):
        newNode = QueueNode(card)
        if self.rear is None:
            self.front = self.rear = newNode
        else:
            self.rear.next = newNode
            self.rear = newNode

    def dequeue(self):
        if self.isEmpty():
            print("StockPile is empty")
            return None

        removeCard = self.front.card
        self.front = self.front.next
        if self.front is None:
            self.rear = None

        return removeCard

    def PeekFront(self):
        if self.isEmpty():
            print("StockPile is empty.")
            return None
        return self.front.card


    def displayStockPile(self):
        current = self.front
        while current is not None:
            print(current.card)
            current = current.next

        