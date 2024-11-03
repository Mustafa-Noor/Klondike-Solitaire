from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
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

        self.cards = InitializeDeck()
        print(len(self.cards))
        self.stockPile = StockPileClass()
        self.wastePile = StockPileClass()
        self.tableauColumns = [TableauPile() for i in range(7)]

        PrepareGame(self.cards,self.stockPile, self.tableauColumns)
        self.updateTableau()

        

        self.stockLabel = self.findChild(QLabel, "Stockpile")
        self.CardFromStock = self.findChild(QLabel, "CardFromStock")
        self.SpadesPile = self.findChild(QLabel, "spadesPile")
        self.HeartsPile = self.findChild(QLabel, "heartsPile")
        self.ClubsPile = self.findChild(QLabel, "clubsPile")
        self.DiamondsPile = self.findChild(QLabel, "diamondsPile")


        self.stockLabel.mousePressEvent = lambda event: self.HandleStockPile()
        self.CardFromStock.mousePressEvent = lambda event: self.clicker("cards")
        self.SpadesPile.mousePressEvent = lambda event: self.clicker("spades")
        self.HeartsPile.mousePressEvent = lambda event: self.clicker("hearts")
        self.ClubsPile.mousePressEvent = lambda event: self.clicker("clubs")
        self.DiamondsPile.mousePressEvent = lambda event: self.clicker("diamonds")

        # show tha application
        self.show()


    def clicker(self, sen):
        print(sen)

    def updateTableau(self):
        yOffset = 50  

        for i, tableau in enumerate(self.tableauColumns):
            columnLabel = self.findChild(QLabel, f"column{i+1}")

            # Check if columnLabel exists
            if columnLabel is None:
                print(f"Column {i+1} QLabel not found!")
                continue

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
                    
                setImage(label, current.card.getCardImage())
                label.setGeometry(xGeometry, yGeometry+(yOffset*cardNo), width, height)
                label.setScaledContents(True)
                label.show()

                current = current.next
                
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


def setImage(label, imageAddress):
    pixmap = QPixmap(imageAddress)
    label.setPixmap(pixmap)
    label.setScaledContents(True)


def removeImage(label):
    label.clear()


def PrepareGame(cards, stockPile, tableauColumns):

    #prepare the tableau columns
    for i in range(7):
        for j in range(i+1):
            tableauColumns[i].push(cards.pop(0))

    # prepare the stockpile
    for i in range(len(cards)):
        stockPile.enqueue(cards.pop(0))





# initialize the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()