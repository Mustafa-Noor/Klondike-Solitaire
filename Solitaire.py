from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys


from CardClass import InitializeDeck, ShuffleCards
from stockpile import StockPileClass
import random


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # LOAD THE UI FILE

        uic.loadUi("SolitaireUI.ui", self)

        self.cards = InitializeDeck()
        print(len(self.cards))
        self.stockPile = StockPileClass()

        for i in range(28):
            self.stockPile.enqueue(self.cards.pop(0))

        



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

    def HandleStockPile(self):
        card = self.stockPile.dequeue()

        if card is None:
            self.CardFromStock.clear()

            cards = ShuffleCards(self.cards) 
            self.stockPile.reQueue(cards)

            
            pixmap = QPixmap("SuitsImages/back.jpeg")
            self.stockLabel.setPixmap(pixmap)
            self.stockLabel.setScaledContents(True)
            return

       
        pixmap = QPixmap(card.cardImage)
        self.CardFromStock.setPixmap(pixmap)
        self.CardFromStock.setScaledContents(True)

        
        if self.stockPile.peek() is None:
            self.stockLabel.clear()


def removeImage(label):
    blank_pixmap = QPixmap()
    label.setPixmap(blank_pixmap)


# initialize the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()