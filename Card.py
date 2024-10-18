class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.isFaceUp = False  # Initially face-down

    # Corrected method to flip the card
    def flipCard(self):
        self.isFaceUp = not self.isFaceUp  # Toggle the face-up/face-down state

    def __str__(self):
        if self.isFaceUp:
            return f"{self.rank} of {self.suit}"
        else:
            return "The card is face down!"


# Dictionary to store the cards with unique card IDs
cards = {}

# Function to add a card to the dictionary
def AddCard(cardID, rank, suit):
    cards[cardID] = Card(rank, suit)  # Create a new Card and add it to the dictionary
    print(f"Added card: {cards[cardID]} with ID '{cardID}'")


# Function to flip a card (flipCard method is part of the Card class)
def flipCard(cardID):
    if cardID in cards:
        cards[cardID].flipCard()  # Call the flipCard method on the Card object
        print(f"Flipped card: {cards[cardID]} with ID '{cardID}'")
    else:
        print(f"Card ID '{cardID}' not found.")


# Function to check the card status
def CheckCardStatus(cardID):
    if cardID in cards:
        card = cards[cardID]
        return str(card), card.isFaceUp  # Return string representation and state (face-up or face-down)
    return None


# Function to initialize a standard deck of cards
def InitializeDeck():
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    for suit in suits:
        for rank in ranks:
            cardID = f"{rank}-{suit}"  # Unique identifier for each card, e.g., 'A-Hearts'
            AddCard(cardID, rank, suit)  # Add the card to the dictionary


# Function to display all cards and their statuses
def displayAllCards():
    print("\nAll Cards in the HashMap:")
    for cardID, card in cards.items():
        print(f"ID: {cardID}, Card: {card}")


# Initialize the deck
InitializeDeck()

# Example usage

print("\nChecking card status:")
status = CheckCardStatus('A-Hearts')  # Check the status of a specific card
if status:
    print(f"Card Status: {status[0]}, Is Face Up: {status[1]}")

print("\nFlipping a card:")
flipCard('A-Hearts')  # Flip the card

print("\nChecking the status again:")
status = CheckCardStatus('A-Hearts')  # Check the status of the flipped card
if status:
    print(f"Card Status: {status[0]}, Is Face Up: {status[1]}")

# Display all cards
displayAllCards()
