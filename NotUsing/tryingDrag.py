from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QMouseEvent
from PyQt5.QtCore import Qt, QMimeData, QPoint
import sys

from CardClass import InitializeDeck, ShuffleCards
from stockpile import StockPileClass
from Tableau import TableauPile
import random

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # LOAD THE UI FILE
        uic.loadUi("SolitaireUI.ui", self)

        # Initialize the deck, stockpile, and tableau columns
        self.cards = InitializeDeck()
        self.stockPile = StockPileClass()
        self.wastePile = StockPileClass()
        self.tableauColumns = [TableauPile() for i in range(7)]

        PrepareGame(self.cards, self.stockPile, self.tableauColumns)
        self.updateTableau()

        # Find labels for piles and connect click events
        self.stockLabel = self.findChild(QLabel, "Stockpile")
        self.CardFromStock = self.findChild(QLabel, "CardFromStock")
        self.SpadesPile = self.findChild(QLabel, "spadesPile")
        self.HeartsPile = self.findChild(QLabel, "heartsPile")
        self.ClubsPile = self.findChild(QLabel, "clubsPile")
        self.DiamondsPile = self.findChild(QLabel, "diamondsPile")

        self.stockLabel.mousePressEvent = lambda event: self.HandleStockPile()
        
        # Initialize variables for selected card and column
        self.selectedCard = None
        self.selectedColumn = None

        # Show the application
        self.show()

    from PyQt5.QtWidgets import QLabel

    def updateTableau(self):
        """Display all tableau columns with updated card positions and enable drops."""
        yOffset = 50  

        for i, tableau in enumerate(self.tableauColumns):
            columnLabel = self.findChild(QLabel, f"column{i+1}")

            if columnLabel is None:
                print(f"Column {i+1} QLabel not found!")
                continue

            # Enable the column label to accept drops
            columnLabel.setAcceptDrops(True)
            columnLabel.dragEnterEvent = self.dragEnterEvent
            columnLabel.dropEvent = lambda event, col=i: self.handleDrop(event, col)

            xGeometry = columnLabel.x()
            yGeometry = columnLabel.y()
            width = columnLabel.width()
            height = columnLabel.height()

            current = tableau.head
            cardNo = 0 
            while current:
                label = QLabel(columnLabel.parent())
                if current.next is None:
                    current.card.flipCard()
                self.setImage(label, current.card.getCardImage())
                label.setGeometry(xGeometry, yGeometry + (yOffset * cardNo), width, height)
                label.setScaledContents(True)
                label.show()

                current = current.next
                cardNo += 1

    def dragEnterEvent(self, event):
        """Accept the drag event."""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def handleDrop(self, event, targetColumn):
        """Handle dropping a card onto a target column."""
        sourceColumn = self.selectedColumn  # Column where drag started
        card = self.selectedCard  # Card being dragged

        if sourceColumn is not None and card:
            # Check if move is valid before moving
            targetTableau = self.tableauColumns[targetColumn]
            
            # Ensure we can only drop onto a column that has cards or is empty
            if targetTableau.isEmpty() or targetTableau.is_valid_move(card):
                # If the target column has cards, get the top card position
                if not targetTableau.isEmpty():
                    top_card = targetTableau.peek()  # Assuming peek gives the top card
                    # Get the position of the top card for offset
                    yOffset = self.calculateDropPosition(targetColumn)

                    # Remove card from source and add it to target
                    self.tableauColumns[sourceColumn].remove(card)
                    targetTableau.push(card)

                    # Update the display to reflect changes
                    self.updateTableau()
                    
                    # Move the card to the calculated drop position
                    card_label = self.findChild(QLabel, card.cardImage)  # Find the QLabel for the card
                    card_label.move(card_label.x(), yOffset)

                    print(f"Moved card {card} from column {sourceColumn + 1} to {targetColumn + 1}")
                else:
                    # If target column is empty, just push the card
                    self.tableauColumns[sourceColumn].remove(card)
                    targetTableau.push(card)
                    self.updateTableau()
                    print(f"Moved card {card} from column {sourceColumn + 1} to empty column {targetColumn + 1}")
            else:
                print("Invalid move")
        else:
            print("Source column or card not set")

        # Reset selected values
        self.selectedCard = None
        self.selectedColumn = None
        event.accept()

    def calculateDropPosition(self, targetColumn):
        """Calculate the Y offset for the card being dropped on the target column."""
        tableau = self.tableauColumns[targetColumn]
        # Calculate the drop position based on the number of cards in the target tableau
        yOffset = 50 * tableau.size()  # Adjust 50 based on your card height
        return yOffset



    from PyQt5.QtCore import Qt, QMimeData
    from PyQt5.QtGui import QDrag

    def startDrag(self, event, label):
        """Initiate dragging of a card QLabel."""
        if event.button() == Qt.LeftButton:
            # Start a drag operation with the label's pixmap
            drag = QDrag(label)
            mimeData = QMimeData()
            mimeData.setText(label.objectName())  # Optionally set card identity
            drag.setMimeData(mimeData)
            drag.setPixmap(label.pixmap())
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.MoveAction)


    def selectCard(self, event, card, column):
        """Handle card selection for movement."""
        if self.selectedCard is None:
            # First click: select the card
            self.selectedCard = card
            self.selectedColumn = column
            print(f"Selected {card} from column {column + 1}")
        else:
            # Second click: attempt to move selected card to target column
            self.moveCardToColumn(column)

    def moveCardToColumn(self, targetColumn):
        """Handle moving the selected card to a target column."""
        # Ensure a card is selected before moving
        if not self.selectedCard or self.selectedColumn is None:
            return

        targetTableau = self.tableauColumns[targetColumn]
        sourceTableau = self.tableauColumns[self.selectedColumn]

        # Check if move is valid (assuming `is_valid_move` method exists in TableauPile)
        if targetTableau.is_valid_move(self.selectedCard):
            # Remove card from source tableau and add it to the target
            sourceTableau.remove(self.selectedCard)
            targetTableau.push(self.selectedCard)

            # Update the display to reflect changes
            self.updateTableau()

            print(f"Moved {self.selectedCard} from column {self.selectedColumn + 1} to column {targetColumn + 1}")

        else:
            print(f"Move of {self.selectedCard} to column {targetColumn + 1} is not valid.")

        # Reset selected card and column
        self.selectedCard = None
        self.selectedColumn = None

    def HandleStockPile(self):
        """Handle click event for stockpile to draw a card."""
        card = handleDequeue(self.stockPile, self.wastePile)
        if card is None:
            removeImage(self.CardFromStock)
            requeueCards(self.stockPile, self.wastePile)
            setImage(self.stockLabel, "SuitsImages/back.jpeg")
            return

        setImage(self.CardFromStock, card.cardImage)
        if self.stockPile.peek() is None:
            removeImage(self.stockLabel)

    def setImage(self, label, imageAddress):
        """Set the image of a QLabel and enable dragging."""
        pixmap = QPixmap(imageAddress)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
    
    # Enable dragging by setting mouse press and mouse move events
        label.setAttribute(Qt.WA_DeleteOnClose)  # Optional: cleans up label after drop
        label.mousePressEvent = lambda event, lbl=label: self.startDrag(event, lbl)

def handleDequeue(stockPile, wastePile):
    """Move a card from the stockpile to the waste pile."""
    card = stockPile.dequeue()
    if card:
        wastePile.enqueue(card)
    return card

def requeueCards(stockPile, wastePile):
    """Requeue cards from the waste pile to the stockpile and shuffle them."""
    cards = []
    while not wastePile.isEmpty():
        cards.append(wastePile.dequeue())
    
    cards = ShuffleCards(cards)
    stockPile.reQueue(cards)



def removeImage(label):
    """Clear the image from a QLabel."""
    label.clear()

def PrepareGame(cards, stockPile, tableauColumns):
    """Initialize the game by distributing cards to tableau columns and stockpile."""
    for i in range(7):
        for j in range(i+1):
            tableauColumns[i].push(cards.pop(0))

    # Populate the stockpile with remaining cards
    for i in range(len(cards)):
        stockPile.enqueue(cards.pop(0))

# Initialize the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
