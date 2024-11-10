class StockPileClass:
    def __init__(self): # constructor of the class
        self.data = []
        self.front = 0
        self.rear = -1
    
    # check is the queue is empty or not
    def isEmpty(self):
        if self.front > self.rear:
            print("Stockpile is empty!!!")
            return True
        return False
        
    # adds a card at the rear of the queue
    def enqueue(self,card):
        if(self.isEmpty()):
            self.front = 0

        self.rear += 1
        if len(self.data) > self.rear:
            self.data[self.rear] = card
        else:
            self.data.append(card)

    # remove a card from the front of the quueue
    def dequeue(self):
        if(self.isEmpty()):
            return
        else:
            card = self.data[self.front]
            self.front += 1
            return card


    # returns the card from the front of the queue
    def peek(self):
        if(self.isEmpty()):
            return
        else:
            card = self.data[self.front]
            return card

    # return the size of the queue
    def giveSize(self):
        return len(data)

    # replace given with its own list
    def reQueue(self,cards):
        self.data = list(cards)
        self.front = 0
        self.rear = len(cards) - 1





        

