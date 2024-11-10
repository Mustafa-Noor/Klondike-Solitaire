from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer, QElapsedTimer
import sys


from CardClass import InitializeDeck, ShuffleCards
from stockpile import StockPileClass
from FoundationStack import Stack
from Tableau import TableauPile
from TableauColumn import TableauColumnClass
from LinkedList import LinkedListCards
from Dictionary import Dictionaries
from ScoreClass import Score
import random


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # LOAD THE UI FILE

        uic.loadUi("SolitaireUI.ui", self)
        self.startTimer()


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)

        self.scoreObject = Score()


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


        self.stackForUndo = Stack()
        self.sourceLabel = None
        self.destinationLabel = None


        self.undoButton = self.findChild(QPushButton, "undo")

        self.dictionary = Dictionaries()

        PrepareGame(self.cards,self.stockPile, self.tableauColumns, self.dictionary, self.LinkedList)

        
        self.updateTableau()


        self.firstSelected = None
        self.secondSelected = None
        self.currentStockCard = None
        self.currentFoundationCard = None
        self.tableauTable = []  
        



        self.clockLabel = self.findChild(QLabel, "clock")
        self.scoreLabel = self.findChild(QLabel, "score")


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

        if self.undoButton is not None:
            self.undoButton.clicked.connect(self.manageUndo)
        else:
            print("button not found")

        

        
        self.initializeTableauLabels()

        self.show()

    def initializeTableauLabels(self):
        self.tableauTable.clear()
        lastLabel = None
        for i in range(7):
            for cardNo in range(self.tableauColumns[i].getSize()+self.LinkedList[i].getSize()):  
                label = self.findChild(QLabel, f"column{i+1}_label_{cardNo}")
                if label is not None:
                    print(f"Label column{i+1}_label_{cardNo} found!")
                    self.tableauTable.append(label)
                    label.mousePressEvent = lambda event, lbl=label: self.checkClick(lbl)
                    lastLabel = label


    def updateScore(self):
        self.scoreLabel.setText(f"Score : {str(self.scoreObject.getScore())}")


    def startTimer(self):
        self.eTimer = QElapsedTimer()
        self.eTimer.start()
                

    def updateClock(self):
        time = self.eTimer.elapsed()
        seconds = (time//1000)%60
        mins = (time // (1000*60))%60
        hours = (time // (1000*60*60))%24
        timeString = f"{hours:02}:{mins:02}:{seconds:02}"
        self.clockLabel.setText(timeString)

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
        count = 0
        columnSource = extractColumn(labelSource.objectName())
        columnDes = extractColumn(labelDes.objectName())

        print("source column:" , columnSource)
        print("destination column:", columnDes)

        if labelSource.objectName() == labelDes.objectName():
            self.deselectCards()
            return

        if checkDestination(labelSource.objectName()) and labelDes.objectName() == "CardFromStock":
            print("cant move from foundation to stock")
            self.deselectCards()
            return
        if checkDestination(labelSource.objectName()) and checkDestination(labelDes.objectName()):
            self.deselectCards()
            return

        # this is for the movement from stockpile to columns
        if labelSource.objectName() == "CardFromStock" and not checkDestination(labelDes.objectName()):
            card = self.currentStockCard
            if card is not None:
                cardDes = self.LinkedList[extractColumnNumber(columnDes)-1].peakLast()
                if self.checkValidMove(card, cardDes):
                    self.moveFromStockToColumn(columnDes, card)
                    self.dictionary.AddtoTableauDict(f"column{extractColumnNumber(columnDes)}", card)
                    self.takeReferencesForUndo(labelSource, labelDes)
                else:
                    self.deselectCards()

        # this is to move from foundation to columns
        elif checkDestination(labelSource.objectName()) and isColumnLabel(labelDes):
            stack = self.findFoundation(labelSource)
            if stack:
                print(stack.getSize())
            card = stack.peak()
            if card is not None:
                print(card.getCardDetail())
                cardDes = self.LinkedList[extractColumnNumber(columnDes)-1].peakLast()
                if self.checkValidMove(card, cardDes):
                    self.updateFoundationPile(stack, labelSource)
                    self.moveFromFoundationToCol(columnDes, card, labelSource)
                    self.dictionary.RemoveFromFoundationDict(labelSource.objectName(), card)
                    self.dictionary.AddtoTableauDict(extractColumnNumber(columnDes),card)
                    self.scoreObject.removePoints(5)
                    self.takeReferencesForUndo(labelSource, labelDes)

                else:
                    self.deselectCards()
            else:
                print("card is empty")


        # this is for the movement of card from either stockpile or columns to foundation pile of spade
        elif labelDes.objectName().lower() == "spadespile":
            if labelSource.objectName() == "CardFromStock":
                card = self.currentStockCard
                if card is not None:
                    print(f"Current Stock Card: {card.getCardDetail()}")
                    if self.checkForSpadesFoundation(card):
                        print("Move valid")
                        self.foundationSpades.push(card)
                        manageStateOfCard(card, self.dictionary, True)
                        self.HandleWastePile()
                        setImage(self.SpadesPile, card.getCardImage())
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
            else:
                card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast()
                if card is not None:
                    if self.checkForSpadesFoundation(card):
                        self.foundationSpades.push(card)
                        self.movefromColToFoundation(self.SpadesPile, columnSource, card)
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        labelSource.clear()
                        labelSource.hide()
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                    else:
                        print("card not according to spade foundation criteria")


        # this is for the movement of card from either stockpile or columns to foundation pile of hearts
        elif labelDes.objectName().lower() == "heartspile":
            if labelSource.objectName() == "CardFromStock":
                card = self.currentStockCard
                if card is not None:
                    if self.checkForHeartsFoundation(card):
                        self.foundationHearts.push(card)
                        manageStateOfCard(card, self.dictionary, True)
                        self.HandleWastePile()
                        setImage(self.HeartsPile, card.getCardImage())
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
            else:
                card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast()
                if card is not None:
                    if self.checkForHeartsFoundation(card):
                        self.foundationHearts.push(card)
                        self.movefromColToFoundation(self.HeartsPile, columnSource, card)
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        labelSource.clear()
                        labelSource.hide()
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                    else:
                        print("card not according to hearts foundation criteria")


        # this is for the movement of card from either stockpile or columns to foundation pile of clubs
        elif labelDes.objectName().lower() == "clubspile":
            if labelSource.objectName() == "CardFromStock":
                card = self.currentStockCard
                if card is not None:
                    if self.checkForClubsFoundation(card):
                        self.foundationClubs.push(card)
                        manageStateOfCard(card, self.dictionary, True)
                        self.HandleWastePile()
                        setImage(self.ClubsPile, card.getCardImage())
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
            else:
                card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast()
                if card is not None:
                    if self.checkForClubsFoundation(card):
                        self.foundationClubs.push(card)
                        self.movefromColToFoundation(self.ClubsPile, columnSource, card)
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        labelSource.clear()
                        labelSource.hide()
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                    else:
                        print("card not according to clubs foundation criteria")



        # this is for the movement of card from either stockpile or columns to foundation pile of diamonds
        elif labelDes.objectName().lower() == "diamondspile":
            if labelSource.objectName() == "CardFromStock":
                card = self.currentStockCard
                if card is not None:
                    if self.checkForDiamondsFoundation(card):
                        self.foundationDiamonds.push(card)
                        manageStateOfCard(card, self.dictionary, True)
                        self.HandleWastePile()
                        setImage(self.DiamondsPile, card.getCardImage())
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
            else:
                card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast()
                if card is not None:
                    if self.checkForDiamondsFoundation(card):
                        self.foundationDiamonds.push(card)
                        self.movefromColToFoundation(self.DiamondsPile, columnSource, card)
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        labelSource.clear()
                        labelSource.hide()
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                    else:
                        print("card not according to diamonds foundation criteria")


        elif checkForColToCol(labelSource, labelDes):
            
            columnNumber = extractColumnNumber(columnSource)
            index = self.calculateIndexOfList(labelSource)
            node = self.LinkedList[columnNumber-1].returnNodeAtIndex(index)
            
            if node is not None:
                print(node.card.getCardDetail())
                cardDes = self.LinkedList[extractColumnNumber(columnDes)-1].peakLast()
                if self.checkValidMove(node.card, cardDes):
                    count = self.AddCardsInColumnList(extractColumnNumber(columnDes)-1, node)
                    current = node
                    while current is not None:
                        self.dictionary.AddtoTableauDict(extractColumnNumber(columnDes), current.card)
                        self.dictionary.RemoveFromTableauDict(columnNumber, current.card)
                        current = current.next
                    
                    self.takeReferencesForUndo(labelSource, labelDes)
                    self.scoreObject.addPoints(5)
                else:
                    current = node
                    while current is not None:
                        self.dictionary.AddtoTableauDict(extractColumnNumber(columnDes), current.card)
                        self.dictionary.RemoveFromTableauDict(columnNumber, current.card)
                        current = current.next

                    self.AddCardsInColumnList(columnNumber-1, node)
                    self.deselectCards()
            else:
                print("node is empty")




        # this is to check if source is a column and if needs to pop a card
        if isColumnLabel(labelSource):
            if self.LinkedList[extractColumnNumber(columnSource)-1].getSize() == 0:
                self.moveCardFromStackToList(extractColumnNumber(columnSource)-1)

                

            columnNumber = int(labelSource.objectName().split('_')[0][6])  
            labelNumber = int(labelSource.objectName().split('_')[2])
            self.clearRemLabels(labelNumber, count+labelNumber, columnNumber)
                
            

        self.updateTableau()
        self.initializeTableauLabels()
        self.updateScore()

        self.checkWinCondition()

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
                    manageStateOfCard(currentNode.card, self.dictionary, True)
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
            if tableauSize == 0 and linkedListSize == 0:
                placeholderLabel = self.findChild(QLabel, f"column{i+1}_placeholder")
                if placeholderLabel is None:
                    placeholderLabel = QLabel(columnLabel.parent())
                    placeholderLabel.setObjectName(f"column{i+1}_placeholder")
                    placeholderLabel.setGeometry(xGeometry, yGeometry, width, height)
                    placeholderLabel.setStyleSheet("border: 2px solid grey; padding: 5px;")

                    
                # Set mouse event to allow dropping cards here
                placeholderLabel.mousePressEvent = lambda event, lbl=placeholderLabel: self.checkClick(lbl)
                placeholderLabel.show()
            else:
                # Hide placeholder if not needed
                placeholderLabel = self.findChild(QLabel, f"column{i+1}_placeholder")
                if placeholderLabel:
                    placeholderLabel.hide()




    def movefromColToFoundation(self, label, columnSource, card):
        setImage(label, card.getCardImage())
        card = self.LinkedList[extractColumnNumber(columnSource)-1].removeCardFromLast()
        print(card.getCardDetail())
        self.dictionary.RemoveFromTableauDict(f"column{columnSource}", card)

    def moveCardFromStackToList(self, column):
        if not self.tableauColumns[column].isEmpty():
            card = self.tableauColumns[column].pop()
            self.AddCardInColumnList(column, card)
            self.dictionary.AddtoTableauDict(f"column{column+1}", card)
            self.scoreObject.addPoints(10)

    def calculateIndexOfList(self, label):
        columnNumber = int(label.objectName().split('_')[0][6])  
        labelNumber = int(label.objectName().split('_')[2])
        print("columNumber", columnNumber)
        print("labelNumber", labelNumber)
        index = labelNumber - self.tableauColumns[columnNumber-1].getSize()
        print(index)
        return index

    

    def takeReferencesForUndo(self, labelSource, labelDes):
        self.sourceLabel = labelDes
        self.destinationLabel = labelSource

    def undoFromColumnToFoundation(self):
        self.tryingMovement(self.sourceLabel, self.destinationLabel)

    def undoFromColumnToStock(self):
        columnNumberOfDes = extractColumnNumber(extractColumn(self.sourceLabel.objectName()))-1

        # column = extractColumn(self.sourceLabel.objectName())
        card = self.LinkedList[columnNumberOfDes].removeCardFromLast()
        self.wastePile.push(card)
        self.currentStockCard = self.wastePile.peak()
        self.updateWastePileForUndo()

        totalSize = self.tableauColumns[columnNumberOfDes].getSize() + self.LinkedList[columnNumberOfDes].getSize()

        # for i in range(0, totalSize):
        #     label = self.findChild(QLabel, f"column{column}_label_{i}")
        #     if label is not None:
        #         label.clear()
        #         label.hide()

        self.sourceLabel.clear()
        self.sourceLabel.hide()
        self.scoreObject.removePoints(20)
        self.sourceLabel = None
        self.destinationLabel = None


        self.updateScore()
        self.updateTableau()
        self.initializeTableauLabels()



    def manageUndo(self):
        if self.sourceLabel is not None and self.destinationLabel is not None:
            print(self.sourceLabel.objectName())
            print(self.destinationLabel.objectName())
            if isColumnLabel(self.sourceLabel) and checkDestination(self.destinationLabel.objectName()):

                self.undoFromColumnToFoundation()

            elif checkDestination(self.sourceLabel.objectName()):
                if self.destinationLabel.objectName() == "CardFromStock":
                    self.undoFromFoundationToStock()
                else:
                    self.sourceLabel = self.findChild(QLabel, extractColumn(self.sourceLabel.objectName())) 
                    self.undoFromFoundationToColumn()

            elif self.destinationLabel.objectName() == "CardFromStock":
                 self.undoFromColumnToStock()
                
            elif isColumnLabel(self.sourceLabel) and isColumnLabel(self.destinationLabel):
                # self.tryingMovement(self.sourceLabel, self.destinationLabel)
                self.undoFromColToCol()

            else:
                print("nahi mila")

            self.sourceLabel = None
            self.destinationLabel = None
        else:
            print("abhi khali hai")

    def undoFromColToCol(self):
        
        count = 0
        columnNumberOfDes = extractColumnNumber(extractColumn(self.destinationLabel.objectName()))-1
        columnNumberOfSource = extractColumnNumber(extractColumn(self.sourceLabel.objectName()))-1

        if self.LinkedList[columnNumberOfDes].getSize() > 1 or self.LinkedList[columnNumberOfDes].getSize() < 1:
            index = self.calculateIndexOfList(self.sourceLabel)
            node = self.LinkedList[columnNumberOfSource].returnNodeAtIndex(index+1)
            if node is not None:
                print(node.card.getCardDetail())
                count = self.AddCardsInColumnList(columnNumberOfDes, node)
            else:
                print("nonenenene")

        elif self.LinkedList[columnNumberOfDes].getSize() == 1:
            card = self.LinkedList[columnNumberOfDes].removeCardFromLast()
            self.tableauColumns[columnNumberOfDes].push(card)
            print(self.sourceLabel.objectName())
            index = self.calculateIndexOfList(self.sourceLabel)
            node = self.LinkedList[columnNumberOfSource].returnNodeAtIndex(index+1)
            if node is not None:
                print(node.card.getCardDetail())
                count = self.AddCardsInColumnList(columnNumberOfDes, node)
            else:
                print("nonenenene")

        
        columnNumber = int(self.sourceLabel.objectName().split('_')[0][6])  
        labelNumber = int(self.sourceLabel.objectName().split('_')[2])
        self.clearRemLabels(labelNumber, count+labelNumber, columnNumber)
        self.updateTableau()
        self.initializeTableauLabels()

            


    def undoFromFoundationToStock(self):
        stack = self.findFoundation(self.sourceLabel)
        if stack:
            print(stack.getSize())
        newCard = stack.pop()
        self.wastePile.push(newCard)
        self.currentStockCard = self.wastePile.peak()
        self.updateWastePileForUndo()
        self.sourceLabel.clear()
        self.scoreObject.removePoints(20)
        self.sourceLabel = None
        self.destinationLabel = None

    def undoFromFoundationToColumn(self):
        columnNumberOfDes = extractColumnNumber(extractColumn(self.destinationLabel.objectName()))-1

        if self.LinkedList[columnNumberOfDes].getSize() > 1 or self.LinkedList[columnNumberOfDes].getSize() < 1:
            self.tryingMovement(self.sourceLabel, self.destinationLabel)
            self.scoreObject.removePoints(20)
        elif self.LinkedList[columnNumberOfDes].getSize() == 1:
            card = self.LinkedList[columnNumberOfDes].removeCardFromLast()
            self.tableauColumns[columnNumberOfDes].push(card)
            stack = self.findFoundation(self.sourceLabel)
            if stack:
                print(stack.getSize())
            newCard = stack.pop()
            self.LinkedList[columnNumberOfDes].AddCard(newCard)
            print(stack.getSize())
            self.sourceLabel.clear()
            self.scoreObject.removePoints(20)

        self.updateScore()
        self.updateTableau()
        self.initializeTableauLabels()

            

        





        
    def checkWinCondition(self):
        # Check if all foundation piles have 13 cards
        if (self.foundationSpades.getSize() == 13 and
            self.foundationHearts.getSize() == 13 and
            self.foundationClubs.getSize() == 13 and
            self.foundationDiamonds.getSize() == 13):
            
            # Show message box if the win condition is met
            self.showWinMessage()

    def showWinMessage(self):
        # Create and display the win message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("You Win!")
        msg.setWindowTitle("Game Over")
        msg.exec_()

    def moveFromStockToColumn(self, columnDes, card):
        self.AddCardInColumnList(extractColumnNumber(columnDes)-1, card)
        self.HandleWastePile()
        self.dictionary.AddtoTableauDict(f"column{columnDes}", card)


    def moveFromFoundationToCol(self, columnDes, card, label):
        self.AddCardInColumnList(extractColumnNumber(columnDes)-1, card)
        self.dictionary.AddtoTableauDict(f"column{columnDes}", card)


    def AddCardInColumnList(self, columnNumber, card):

        if card is not None:  # Ensure that card is not None
            self.LinkedList[columnNumber].AddCard(card)
            print(f"Card {card.getCardDetail()} added to column {columnNumber + 1}")
            
        else:
            print("Cannot add empty card to linked list")

    def AddCardsInColumnList(self, columnNumber, node):

        count = 0
        if node is not None:  # Ensure that card is not None
           count =  self.LinkedList[columnNumber].AddCards(node)
        else:
            print("Cannot add empty nodd to linked list")
        
        return count

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
    
        manageStateOfCard(card, self.dictionary, True)
        setImage(self.CardFromStock, card.getCardImage())
        self.currentStockCard = card
        
        if self.stockPile.peek() is None:
            removeImage(self.stockLabel)

    def peakFromWaste(self):
        return self.wastePile.peak()


    def updateFoundationPile(self, stack, label):
        stack.pop()
        card = stack.peak()
        if card is not None:
            manageStateOfCard(card, self.dictionary, True)
            setImage(label, card.getCardImage())
        else: 
            removeImage(label)

        
    def findFoundation(self, label):
        if label.objectName().lower() == "spadespile":
            return self.foundationSpades
        elif label.objectName().lower() == "heartspile":
            return self.foundationHearts
        elif label.objectName().lower() == "diamondspile":
            return self.foundationDiamonds
        elif label.objectName().lower() == "clubspile":
            return self.foundationClubs

    def updateWastePile(self):
        self.wastePile.pop()
        card = self.wastePile.peak()
        
        if card is not None:
            manageStateOfCard(card, self.dictionary, True)
            setImage(self.CardFromStock, card.getCardImage())
            self.currentStockCard = card
        else: 
            removeImage(self.CardFromStock)
            self.currentStockCard = None

    def HandleWastePile(self):
        self.currentStockCard = self.peakFromWaste()
        self.updateWastePile()

    def checkValidMove(self,card1, card2):
        if card2 is None:
            #means moving card to empty column
            return True

        if self.dictionary.getRank(card1.rank) != self.dictionary.getRank(card2.rank)-1:
            print(card1.getCardDetail())
            print(card2.getCardDetail())
            print("not valid", card1.rank, "  ", card2.rank)
            return False

        if self.dictionary.colourMap[card1.suit.lower()] == self.dictionary.colourMap[card2.suit.lower()]:
            print("not valid", card1.suit, "  ", card2.suit)
            return False
        
        return True

    def checkForSpadesFoundation(self, card):
        lastCard = self.foundationSpades.peak()
        if lastCard is not None:
            if card.suit.lower() == "spades" and self.dictionary.getRank(card.rank) == self.dictionary.getRank(lastCard.rank)+1:
                return True
        elif lastCard is None:
            if card.suit.lower() == "spades" and self.dictionary.getRank(card.rank) == 1:
                return True
        else:
            return False


    def checkForHeartsFoundation(self, card):
        lastCard = self.foundationHearts.peak()
        if lastCard is not None:
            if card.suit.lower() == "hearts" and self.dictionary.getRank(card.rank) == self.dictionary.getRank(lastCard.rank)+1:
                return True
        elif lastCard is None:
            if card.suit.lower() == "hearts" and self.dictionary.getRank(card.rank) == 1:
                return True
        else:
            return False

    def checkForClubsFoundation(self, card):
        lastCard = self.foundationClubs.peak()
        if lastCard is not None:
            if card.suit.lower() == "clubs" and self.dictionary.getRank(card.rank) == self.dictionary.getRank(lastCard.rank)+1:
                return True
        elif lastCard is None:
            if card.suit.lower() == "clubs" and self.dictionary.getRank(card.rank) == 1:
                return True
        else:
            return False


    def checkForDiamondsFoundation(self, card):
        lastCard = self.foundationDiamonds.peak()

        if lastCard is not None:
            if card.suit.lower() == "diamonds" and self.dictionary.getRank(card.rank) == self.dictionary.getRank(lastCard.rank)+1:
                return True
        elif lastCard is None:
            if card.suit.lower() == "diamonds" and self.dictionary.getRank(card.rank) == 1:
                return True
        else:
            return False

    def clearRemLabels(self,start, end, column):
        for i in range(start, end+13):
            label = self.findChild(QLabel, f"column{column}_label_{i}")
            if label is not None:
                label.clear()
                label.hide()

    def updateWastePileForUndo(self):
        card = self.wastePile.peak()
        
        if card is not None:
            manageStateOfCard(card, self.dictionary, True)
            setImage(self.CardFromStock, card.getCardImage())
            self.currentStockCard = card
        else: 
            removeImage(self.CardFromStock)
            self.currentStockCard = None

    def deselectCards(self):
        removeBorder(self.firstSelected)
        self.firstSelected = None
        removeBorder(self.secondSelected)
        self.secondSelected = None

def checkDestination(sen):
    array = ["spadespile", "heartspile", "clubspile", "diamondspile"]
    if sen.lower() in array:
        return True
    return False


def handleDequeue(stockPile, wastePile):
    card = stockPile.dequeue()
    if card:
        wastePile.push(card)
    return card

def checkForColToCol(labelSource, labelDes):
    if isColumnLabel(labelSource) and isColumnLabel(labelDes):
        print("condition was true")
        return True
    print("condition was false")
    return False


def isColumnLabel(label):
    return label.objectName()[:6] == "column"


def manageStateOfCard(card, dictionary, faceUp):
        dictionary.changeState(card, faceUp)

        

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
    if label is not None:
        label.setStyleSheet("")
        label.update()

 


    
def PrepareGame(cards, stockPile, tableauColumns, dictionary, LinkedList):

    #prepare the tableau columns
    if cards: 
        for i in range(7):
            tempStack = []
            for j in range(i+1):
                card = cards.pop(0)
                if j == i:
                    LinkedList[i].AddCard(card)
                    manageStateOfCard(card, dictionary, True)
                    dictionary.AddtoTableauDict(f"column{i+1}", card)
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







# initialize the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()