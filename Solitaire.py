from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys


from CardClass import InitializeDeck, ShuffleCards
from stockpile import StockPileClass
from Tableau import TableauPile
from TableauColumn import TableauColumnClass
from LinkedList import LinkedListCards
from Dictionary import Dictionaries
import random


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # LOAD THE UI FILE

        uic.loadUi("SolitaireUI.ui", self)

        self.firstInit = True

        self.cards = InitializeDeck()
        print(len(self.cards))
        self.stockPile = StockPileClass()
        self.wastePile = StockPileClass()
        self.tableauColumns = [TableauColumnClass() for i in range(7)]
        self.LinkedList = [LinkedListCards() for i in range(7)]

        self.dictionary = Dictionaries()

        PrepareGame(self.cards,self.stockPile, self.tableauColumns, self.dictionary, self.LinkedList)

        
        self.updateTableau()


        self.firstSelected = None
        self.secondSelected = None
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
        self.tableauTable.clear()
        for i in range(7):
            for cardNo in range(self.tableauColumns[i].getSize()+self.LinkedList[i].getSize()):  # Use the actual number of cards per column
                label = self.findChild(QLabel, f"column{i+1}_label_{cardNo}")
                if label is not None:
                    print(f"Label column{i+1}_label_{cardNo} found!")
                    self.tableauTable.append(label)
                    label.mousePressEvent = lambda event, lbl=label: self.checkClick(lbl)
                else:
                    print(f"Label column{i+1}_label_{cardNo} not found!")
            




    def checkClick(self, label):

        if self.firstSelected is None:
            self.firstSelected = label
            self.firstSelected.setStyleSheet("border: 2px solid black; padding: 5px;")
            self.firstSelected.update()
        else:
            self.secondSelected = label
            self.secondSelected.setStyleSheet("border: 2px solid black; padding: 5px;")
            self.secondSelected.update()
            self.firstSelected.setStyleSheet("")  
            self.firstSelected.update()
            self.tryingMovement(self.firstSelected, self.secondSelected)
            self.firstSelected = None

        if self.secondSelected is not None:
            self.secondSelected.setStyleSheet("")  
            self.secondSelected.update()
            self.secondSelected = None

    def tryingMovement(self, labelSource, labelDes):
        columnSource = extractColumn(labelSource.objectName())
        columnDes = extractColumn(labelDes.objectName())
        print("source column:" , columnSource)
        print(columnDes)
        card = self.tableauColumns[extractColumnNumber(columnSource)-1].pop()
        self.AddCardInColumnList(extractColumnNumber(columnDes)-1, card)
        # self.tableauColumns[extractColumnNumber(columnDes)-1].push(card)
        labelSource.clear()
        labelSource.hide()

        self.updateTableau()
        self.initializeTableauLabels()


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

            # Get the sizes of the tableau column and corresponding LinkedList
            tableauSize = tableau.getSize()
            linkedListSize = self.LinkedList[i].getSize()
            print(f"Tableau size: {tableauSize}, LinkedList size: {linkedListSize}")

            # Display all cards in the tableau, hiding intermediate cards
            for j in range(tableauSize):
                if j < tableauSize - 1 - linkedListSize:  # Back face for non-visible cards
                    cardImage = "SuitsImages/back.jpeg"
                else:  
                    # card = tableau.peak()
                    # card.isFaceUp = True
                    cardImage = card.getCardImage()

                
                label = self.findChild(QLabel, f"column{i+1}_label_{j}")
                if label is None:
                    label = QLabel(columnLabel.parent())
                    label.setObjectName(f"column{i+1}_label_{j}")
                setImage(label, cardImage)
                label.setGeometry(xGeometry, yGeometry + (yOffset * j), width, height)
                label.setScaledContents(True)
                label.show()

            # Display cards in LinkedList if it has additional cards for this column
            currentNode = self.LinkedList[i].head
            for k in range(linkedListSize):
                if currentNode is None:
                    break
                # Set card to face up and get its image
                currentNode.card.isFaceUp = True
                cardImage = currentNode.card.getCardImage()

                # Create or update QLabel for this LinkedList card
                label = self.findChild(QLabel, f"column{i+1}_label_{tableauSize + k}")
                if label is None:
                    label = QLabel(columnLabel.parent())
                    label.setObjectName(f"column{i+1}_label_{tableauSize + k}")
                setImage(label, cardImage)
                label.setGeometry(xGeometry, yGeometry + (yOffset * (tableauSize + k)), width, height)
                label.setScaledContents(True)
                label.show()

                # Move to the next node in the LinkedList
                currentNode = currentNode.next



        



    def AddCardInColumnList(self, columnNumber, card):
        self.LinkedList[columnNumber].AddCard(card)
        print("added in linked list")

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

def extractColumnNumber(sen):
    return int(sen[6])





def setImage(label, imageAddress):
    pixmap = QPixmap(imageAddress)
    label.setPixmap(pixmap)
    label.setScaledContents(True)


def removeImage(label):
    label.clear()

def giveBackImage():
    return f"SuitsImages/back.jpeg"
    
def PrepareGame(cards, stockPile, tableauColumns, dictionary, LinkedList):

    #prepare the tableau columns
    if cards: 
        for i in range(7):
            for j in range(i+1):
                card = cards.pop(0)
                if j == i:
                    LinkedList[i].AddCard(card)
                else:
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