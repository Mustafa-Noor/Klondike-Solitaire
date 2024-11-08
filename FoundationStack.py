class Stack:
    def __init__(self):
        self.data = []
        self.top = -1

    def push(self,card):
        self.top += 1
        if(self.top>=len(self.data)):
            self.data.append(card)
        else:
            self.data[self.top] = card

    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False

    def pop(self):
        if not self.isEmpty():
            card = self.data[self.top]
            self.top -= 1
            return card
        return None

    def peak(self):
        if not self.isEmpty():
            card = self.data[self.top]
            return card
        return None

    def getSize(self):
        return self.top+1