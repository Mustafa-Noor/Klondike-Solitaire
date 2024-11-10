class TableauColumnClass: 
    def __init__(self): # constructor of the class
        self.data = []
        self.top = -1 # at the beginning top is kept at -1


    # this is to push a card in the array and increment top
    def push(self,card):
        self.top += 1
        if(self.top>=len(self.data)): # if top is greater than array resize array
            self.data.append(card)
        else:
            self.data[self.top] = card

    # this checks if stack is empty
    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False

    # this returns the top card
    def pop(self):
        if not self.isEmpty():
            card = self.data[self.top]
            self.top -= 1
            return card
        return None


    # this returns the top card without losing its refernce
    def peak(self):
        if not self.isEmpty():
            card = self.data[self.top]
            return card
        return None


    # this function checks if there exist atleast one card or not
    def checkNext(self):
        if self.top == -1:
            return True
        return False

    # this return the size of occupied list
    def getSize(self):
        return self.top+1




