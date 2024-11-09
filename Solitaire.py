from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys


from CardClass import InitializeDeck, ShuffleCards
from stockpile import StockPileClass
from FoundationStack import Stack
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


        self.cards = InitializeDeck()
        print(len(self.cards))
        self.stockPile = StockPileClass()
        self.wastePile = Stack()
        self.tableauColumns = [TableauColumnClass() for i in range(7)]
        self.LinkedList = [LinkedListCards() for i in range(7)]
       

        self.foundationSpades = Stack()
        self.foundationHearts = Stack()
        self.foundationClubs = Stack()
        self.foundationDiamonds = Stack()

        self.dictionary = Dictionaries()

        PrepareGame(self.cards,self.stockPile, self.tableauColumns, self.dictionary, self.LinkedList)

        
        self.updateTableau()


        self.firstSelected = None
        self.secondSelected = None
        self.currentStockCard = None
        self.tableauTable = []  
        



        self.stockLabel = self.findChild(QLabel, "Stockpile")
        self.CardFromStock = self.findChild(QLabel, "CardFromStock")
        self.SpadesPile = self.findChild(QLabel, "spadesPile")
        self.HeartsPile = self.findChild(QLabel, "heartsPile")
        self.ClubsPile = self.findChild(QLabel, "clubsPile")
        self.DiamondsPile = self.findChild(QLabel, "diamondsPile")


        self.stockLabel.mousePressEvent = lambda event: self.HandleStockPile()
        self.CardFromStock.mousePressEvent = lambda event: self.checkClick(self.CardFromStock)
        self.SpadesPile.mousePressEvent = lambda event: self.checkClick(self.SpadesPile)
        self.HeartsPile.mousePressEvent = lambda event: self.checkClick(self.HeartsPile)
        self.ClubsPile.mousePressEvent = lambda event: self.checkClick(self.ClubsPile)
        self.DiamondsPile.mousePressEvent = lambda event: self.checkClick(self.DiamondsPile)

        

        
        self.initializeTableauLabels()

        self.show()

    def initializeTableauLabels(self):
        self.tableauTable.clear()
        lastLabel = None
        for i in range(7):
            for cardNo in range(self.tableauColumns[i].getSize()+self.LinkedList[i].getSize()):  # Use the actual number of cards per column
                label = self.findChild(QLabel, f"column{i+1}_label_{cardNo}")
                if label is not None:
                    print(f"Label column{i+1}_label_{cardNo} found!")
                    self.tableauTable.append(label)
                    label.mousePressEvent = lambda event, lbl=label: self.checkClick(lbl)
                    lastLabel = label
                

    def checkClick(self, label):

        if self.firstSelected is None:
            self.firstSelected = label
            giveBorder(self.firstSelected)
        else:
            self.secondSelected = label
            giveBorder(self.secondSelected)
            removeBorder(self.firstSelected)
            self.tryingMovement(self.firstSelected, self.secondSelected)
            self.firstSelected = None

        if self.secondSelected is not None:
            removeBorder(self.secondSelected)
            self.secondSelected = None


    def tryingMovement(self, labelSource, labelDes):
        columnSource = extractColumn(labelSource.objectName())
        columnDes = extractColumn(labelDes.objectName())

        print("source column:" , columnSource)
        print("destination column:", columnDes)

        if labelSource.objectName() == "CardFromStock":
            card = self.currentStockCard
            if card is not None:
                cardDes = self.LinkedList[extractColumnNumber(columnDes)-1].peakLast()
                if self.checkValidMove(card, cardDes):
                    self.AddCardInColumnList(extractColumnNumber(columnDes)-1, card)
                    self.HandleWastePile()
                    self.dictionary.AddtoTableauDict(f"column{columnDes}", card)
                else:
                    removeBorder(self.firstSelected)
                    self.firstSelected = None
                    removeBorder(self.secondSelected)
                    self.secondSelected = None

        elif labelDes.objectName() == "spadesPile":
            card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast()
            if card is not None:
                self.foundationSpades.push(card)
                setImage(self.SpadesPile, card.getCardImage())
                card = self.LinkedList[extractColumnNumber(columnSource)-1].removeCardFromLast()
                print(card.getCardDetail())
                self.dictionary.RemoveFromTableauDict(f"column{columnSource}", card)


        else:
            card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast()
            if card is not None:
                cardDes = self.LinkedList[extractColumnNumber(columnDes)-1].peakLast()
                if self.checkValidMove(card, cardDes):
                    self.AddCardInColumnList(extractColumnNumber(columnDes)-1, card)
                    self.dictionary.AddtoTableauDict(f"column{columnDes}", card)
                    card = self.LinkedList[extractColumnNumber(columnSource)-1].removeCardFromLast()
                    self.dictionary.RemoveFromTableauDict(f"column{columnSource}", card)

                else:
                    removeBorder(self.firstSelected)
                    self.firstSelected = None
                    removeBorder(self.secondSelected)
                    self.secondSelected = None
        # self.tableauColumns[extractColumnNumber(columnDes)-1].push(card)
        if self.LinkedList[extractColumnNumber(columnSource)-1].getSize() == 0:
            self.moveCardFromStackToList(extractColumnNumber(columnSource)-1)
            self.dictionary.RemoveFromTableauDict(f"column{columnSource}", card)
                
                
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

#could be of the use in future
            # for j in range(self.tableauColumns[i].getSize() + self.LinkedList[i].getSize()):
            #     existingLabel = self.findChild(QLabel, f"column{i+1}_label_{j}")
            #     if existingLabel:
            #         existingLabel.clear()
            #         existingLabel.hide()

            # Get the sizes of the tableau column and corresponding LinkedList
            tableauSize = tableau.getSize()
            linkedListSize = self.LinkedList[i].getSize()
            print(f"Tableau size: {tableauSize}, LinkedList size: {linkedListSize}")

            # Display all cards in the tableau, hiding intermediate cards
            for j in range(tableauSize):
                    cardImage = "SuitsImages/back.jpeg"
                    label = self.findChild(QLabel, f"column{i+1}_label_{j}")
                    if label is None:
                        label = QLabel(columnLabel.parent())
                        label.setObjectName(f"column{i+1}_label_{j}")
                    setImage(label, cardImage)
                    label.setGeometry(xGeometry, yGeometry + (yOffset * j), width, height)
                    label.setScaledContents(True)
                    label.show()

            # Traverse the LinkedList for the tableau
            currentNode = self.LinkedList[i].head
            k = 0
            while currentNode is not None:
                if currentNode.card is not None:
                    print(currentNode.card.getCardDetail())
                    currentNode.card.isFaceUp = True  # Flip the card face up
                    cardImage = currentNode.card.getCardImage()
                    label = self.findChild(QLabel, f"column{i+1}_label_{tableauSize + k}")
                    if label is None:
                        label = QLabel(columnLabel.parent())
                        label.setObjectName(f"column{i+1}_label_{tableauSize + k}")
                    setImage(label, cardImage)
                    label.setGeometry(xGeometry, yGeometry + (yOffset * (tableauSize + k)), width, height)
                    label.setScaledContents(True)
                    label.show()

                    # Move to the next node in the LinkedList
                    
                else:
                    print("wasnt there")

                currentNode = currentNode.next
                k=k+1



    def moveCardFromStackToList(self, column):
        if not self.tableauColumns[column].isEmpty():
            card = self.tableauColumns[column].pop()
            self.AddCardInColumnList(column, card)
        



    def AddCardInColumnList(self, columnNumber, card):

        if card is not None:  # Ensure that card is not None
            self.LinkedList[columnNumber].AddCard(card)
            print(f"Card {card.getCardDetail()} added to column {columnNumber + 1}")
            
        else:
            print("Cannot add empty card to linked list")
        

    def removeCardLast(self, columnNumber):
        if not self.LinkedList[columnNumber].isEmpty():
            card = self.LinkedList[columnNumber].removeCardFromLast()
            print(f"Removed card {card.getCardDetail()} from column {columnNumber + 1}")
            return card

        else:
            print("Cannot remove from empty list")
            return None

    def HandleStockPile(self):
        card = handleDequeue(self.stockPile, self.wastePile)
        
        if card is None:
            removeImage(self.CardFromStock)
            requeueCards(self.stockPile, self.wastePile)
            setImage(self.stockLabel,"SuitsImages/back.jpeg")
            return
    
        setImage(self.CardFromStock, card.cardImage)
        self.currentStockCard = card
        
        if self.stockPile.peek() is None:
            removeImage(self.stockLabel)

    def peakFromWaste(self):
        return self.wastePile.peak()

    def updateWastePile(self):
        self.wastePile.pop()
        card = self.wastePile.peak()
        
        if card is not None:
            card.isFaceUp = True
            setImage(self.CardFromStock, card.getCardImage())
            self.currentStockCard = card
        else: 
            removeImage(self.CardFromStock)
            self.currentStockCard = None

    def HandleWastePile(self):
        self.currentStockCard = self.peakFromWaste()
        self.updateWastePile()

    def checkValidMove(self,card1, card2):
        if validateRank(card1.rank) != validateRank(card2.rank)-1:
            return False

        if self.dictionary.colourMap[card1.suit.lower()] == self.dictionary.colourMap[card2.suit.lower()]:
            return False
        
        return True


def handleDequeue(stockPile, wastePile):
    card = stockPile.dequeue()
    if card:
        wastePile.push(card)
    return card



def requeueCards(stockPile, wastePile):
    cards = []
    while not wastePile.isEmpty():
        cards.append(wastePile.pop())
    
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


def giveBorder(label):
    label.setStyleSheet("border: 2px solid black; padding: 5px;")
    label.update()

def removeBorder(label):
    label.setStyleSheet("")
    label.update()




def validateRank(rank):
    if rank == "ace":
        return 1
    elif rank == "jack":
        return 11
    elif  rank == "queen":
        return 12
    elif rank == "king":
        return 13
    else:
        return int(rank)    


    
def PrepareGame(cards, stockPile, tableauColumns, dictionary, LinkedList):

    #prepare the tableau columns
    if cards: 
        for i in range(7):
            tempStack = []
            for j in range(i+1):
                card = cards.pop(0)
                if j == i:
                    LinkedList[i].AddCard(card)
                else:
                    tempStack.append(card)

            while tempStack:
                card = tempStack.pop()
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