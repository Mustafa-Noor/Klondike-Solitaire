from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys


from CardClass import InitializeDeck
import random


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # LOAD THE UI FILE

        uic.loadUi("SolitaireUI.ui", self)

        self.cards = InitializeDeck()


        self.StockPile = self.findChild(QLabel, "Stockpile")
        self.CardFromStock = self.findChild(QLabel, "CardFromStock")
        self.SpadesPile = self.findChild(QLabel, "spadesPile")
        self.HeartsPile = self.findChild(QLabel, "heartsPile")
        self.ClubsPile = self.findChild(QLabel, "clubsPile")
        self.DiamondsPile = self.findChild(QLabel, "diamondsPile")


        self.StockPile.mousePressEvent = lambda event: self.printCards()
        self.CardFromStock.mousePressEvent = lambda event: self.clicker("cards")
        self.SpadesPile.mousePressEvent = lambda event: self.clicker("spades")
        self.HeartsPile.mousePressEvent = lambda event: self.clicker("hearts")
        self.ClubsPile.mousePressEvent = lambda event: self.clicker("clubs")
        self.DiamondsPile.mousePressEvent = lambda event: self.clicker("diamonds")

        # show tha application
        self.show()


    def clicker(self, sen):
        print(sen)

    def printCards(self):
        keys = list(self.cards.keys())
        random.shuffle(keys)
        
        card = self.cards[keys[0]]
        print(card.suit)
        pixmap = QPixmap(card.cardImage)
        self.CardFromStock.setPixmap(pixmap)
        self.CardFromStock.setScaledContents(True)

# initialize the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()