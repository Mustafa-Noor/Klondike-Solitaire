from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys


from CardClass import InitializeDeck, ShuffleCards
from stockpile import StockPileClass
from Tableau import TableauPile
from TableauColumn import TableauColumnClass
from Dictionary import Dictionaries
import random


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # LOAD THE UI FILE

        uic.loadUi("SolitaireUI.ui", self)

        self.cards = InitializeDeck()
        print(len(self.cards))
        self.stockPile = StockPileClass()
        self.wastePile = StockPileClass()
        self.tableauColumns = [TableauPile() for i in range(7)]

        self.dictionary = Dictionaries()

        PrepareGame(self.cards,self.stockPile, self.tableauColumns, self.dictionary)

        self.updateTableau()

        
        

        self.selectedCards = []
        self.tableauTable = []  
        



        self.stockLabel = self.findChild(QLabel, "Stockpile")
        self.CardFromStock = self.findChild(QLabel, "CardFromStock")
        self.SpadesPile = self.findChild(QLabel, "spadesPile")
        self.HeartsPile = self.findChild(QLabel, "heartsPile")
        self.ClubsPile = self.findChild(QLabel, "clubsPile")
        self.DiamondsPile = self.findChild(QLabel, "diamondsPile")


        self.stockLabel.mousePressEvent = lambda event: self.HandleStockPile()
        self.CardFromStock.mousePressEvent = lambda event: self.checkClick(self.CardFromStock)
        self.SpadesPile.mousePressEvent = lambda event: self.clicker("spades")
        self.HeartsPile.mousePressEvent = lambda event: self.clicker("hearts")
        self.ClubsPile.mousePressEvent = lambda event: self.clicker("clubs")
        self.DiamondsPile.mousePressEvent = lambda event: self.clicker("diamonds")

        

        
        self.initializeTableauLabels()

        self.show()

    def initializeTableauLabels(self):
        for i in range(7):
            current = self.tableauColumns[i].head  # Start from the head of the linked list
            cardNo = 0

            while current is not None:  # Traverse until the end of the linked list
                label = self.findChild(QLabel, f"column{i+1}_label_{cardNo}")
                if label is not None:
                    print(f"Label column{i+1}_label_{cardNo} found!")
                    self.tableauTable.append(label)
                    label.mousePressEvent = lambda event, lbl=label: self.checkClick(lbl)
                else:
                    print(f"Label column{i+1}_label_{cardNo} not found!")

                current = current.next  # Move to the next card
                cardNo += 1


    def checkClick(self, label):
        # If the label is already selected, deselect it
        if label in self.selectedCards:
            self.selectedCards.remove(label)
            label.setStyleSheet("")  # Reset style
            label.update()
        else:
            # If two cards are already selected, don't allow selection of more
            if len(self.selectedCards) < 2:
                self.selectedCards.append(label)  # Add to selected cards
                label.setStyleSheet("border: 2px solid black; padding: 5px;")
                label.update()
            else:
                print("Maximum of two cards can be selected.")

        # Debugging output
        column = extractColumn(label.objectName())
        print(f"Selected column: {column}")
        print(f"Currently selected cards: {len(self.selectedCards)}")



        


    def clicker(self, sen):
        print(sen)

    def updateTableau(self):
        yOffset = 50  

        for i, tableau in enumerate(self.tableauColumns):
            columnLabel = self.findChild(QLabel, f"column{i+1}")

            if columnLabel is None:
                print(f"Column {i+1} QLabel not found!")
                continue

            xGeometry = columnLabel.x()
            yGeometry = columnLabel.y()
            width = columnLabel.width()
            height = columnLabel.height()

            cardNo = 0
            current = tableau.head  # Start from the head of the linked list

            while current is not None:  # Traverse the linked list
                card = current.card  # Get the card from the current node
                label = QLabel(columnLabel.parent())
                label.setObjectName(f"column{i+1}_label_{cardNo}")

                if current.next is None:  
                    card.flipCard()

                # Debugging print to check if each card is set correctly
                print(f"Setting image for {label.objectName()}")

                setImage(label, card.getCardImage())
                label.setGeometry(xGeometry, yGeometry + (yOffset * cardNo), width, height)
                label.setScaledContents(True)
                label.show()

                current = current.next  # Move to the next node
                cardNo += 1



    def HandleStockPile(self):
            
            card = handleDequeue(self.stockPile, self.wastePile)
            if card is None:
                removeImage(self.CardFromStock)
                requeueCards(self.stockPile, self.wastePile)
                setImage(self.stockLabel,"SuitsImages/back.jpeg")
                return
        
            setImage(self.CardFromStock, card.cardImage)
            
            if self.stockPile.peek() is None:
                removeImage(self.stockLabel)


def handleDequeue(stockPile, wastePile):
    card = stockPile.dequeue()
    if card:
        wastePile.enqueue(card)
    return card

def requeueCards(stockPile, wastePile):
    cards = []
    while not wastePile.isEmpty():
        cards.append(wastePile.dequeue())
    
    cards = ShuffleCards(cards)
    stockPile.reQueue(cards)

def extractColumn(sen):
    return sen.split('_')[0]


def setImage(label, imageAddress):
    pixmap = QPixmap(imageAddress)
    label.setPixmap(pixmap)
    label.setScaledContents(True)


def removeImage(label):
    label.clear()


def PrepareGame(cards, stockPile, tableauColumns, dictionary):

    #prepare the tableau columns
    if cards: 
        for i in range(7):
            for j in range(i+1):
                card = cards.pop(0)
                tableauColumns[i].push(card)
                dictionary.AddtoTableauDict(f"column{i+1}", card)
                
    else:
        print("no cards to prepare")

    # prepare the stockpile
    for i in range(len(cards)):
        stockPile.enqueue(cards.pop(0))

# theory is that i select a card and the destination card i will check at which place destination card is present using hashmap iwll use that info to append the incoming card label at the end of the destination column

# second approach added it to stack of that column then update
# but find column using hashmap
# def moveCards(col):


# initialize the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()