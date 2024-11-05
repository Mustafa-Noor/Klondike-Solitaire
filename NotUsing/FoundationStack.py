class Stack:
    def _init_(self):
        self.cards = []  # Use a list to store cards

    def push(self, card):
        self.cards.append(card)  # Add a card to the top

    def pop(self):
        return self.cards.pop() if self.cards else None  # Remove and return the top card

    def peek(self):
        return self.cards[-1] if self.cards else None  # Return the top card without removing it

    def is_empty(self):
        return len(self.cards) == 0

    def display(self):
        return " | ".join(str(card) for card in reversed(self.cards))  # Show cards from top to bottom