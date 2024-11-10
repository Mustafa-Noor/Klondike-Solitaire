class Stack:
    def __init__(self): # constructor of the stack
        self.data = []
        self.top = -1

    # push card in the stakc
    def push(self,card):
        self.top += 1
        if(self.top>=len(self.data)):
            self.data.append(card)
        else:
            self.data[self.top] = card

    # check if the stake is empty
    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False
    # pop the card from the stack
    def pop(self):
        if not self.isEmpty():
            card = self.data[self.top]
            self.top -= 1
            return card
        return None

    #gives the card from the top of the stack without removinf
    def peak(self):
        if not self.isEmpty():
            card = self.data[self.top]
            return card
        return None

    # returns the size of the stack
    def getSize(self):
        return self.top+1