class StockPileClass:
    def __init__(self):
        self.data = []
        self.front = 0
        self.rear = -1
    

    def isEmpty(self):
        if self.front > self.rear:
            print("Stockpile is empty!!!")
            return True
        return False
        
            
    def enqueue(self,card):
        if(self.isEmpty()):
            self.front = 0

        self.rear += 1
        if len(self.data) > self.rear:
            self.data[self.rear] = card
        else:
            self.data.append(card)

    def dequeue(self):
        if(self.isEmpty()):
            return
        else:
            card = self.data[self.front]
            self.front += 1
            return card


    def peek(self):
        if(self.isEmpty()):
            return
        else:
            card = self.data[self.front]
            return card




    def giveSize(self):
        return len(data)


    def reQueue(self,cards):
        self.data = list(cards)
        self.front = 0
        self.rear = len(cards) - 1





        

