class FoundationStack:
    def _init_(self):
        self.cards = []  

    def push(self, card):
        self.cards.append(card) 

    def pop(self):
        return self.cards.pop() if self.cards else None 

    def peek(self):
        return self.cards[-1] if self.cards else None  

    def is_empty(self):
        return len(self.cards) == 0

    def display(self):
        return " | ".join(str(card) for card in reversed(self.cards))  