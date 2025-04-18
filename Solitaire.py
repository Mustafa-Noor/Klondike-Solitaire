from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer, QElapsedTimer
import sys




from CardClass import InitializeDeck, ShuffleCards # imports from card class
from stockpile import StockPileClass # imports from stockpile.py
from FoundationStack import Stack   # imports from foundationStock.py  
from TableauColumn import TableauColumnClass # imports from tableauColumn
from LinkedList import LinkedListCards # imports from linkedlist class
from Dictionary import Dictionaries # imports from dictionary class
from ScoreClass import Score # imports from score class
import random


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # LOAD THE UI FILE
        uic.loadUi("SolitaireUI.ui", self)

        # starts timer since the ui loaded
        self.startTimer()

        # sets up a timer which updates itself every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)


        # this is the object of score class
        self.scoreObject = Score()


        # this gets the card from card class
        self.cards = InitializeDeck()
        print(len(self.cards))

        # this initializes stock pile and waste pile
        self.stockPile = StockPileClass()
        self.wastePile = Stack()

        # this initializes 7 columns and 7 linked list for tableau
        self.tableauColumns = [TableauColumnClass() for i in range(7)]
        self.LinkedList = [LinkedListCards() for i in range(7)]
       

        # this is the initialization of the foundation piles
        self.foundationSpades = Stack()
        self.foundationHearts = Stack()
        self.foundationClubs = Stack()
        self.foundationDiamonds = Stack()


        # thsese labels are used during the undo operations
        self.sourceLabel = None
        self.destinationLabel = None


        # this is the undo button
        self.undoButton = self.findChild(QPushButton, "undo")


        # this is the initialization of the dictionary
        self.dictionary = Dictionaries()


        # this functions prepares the game which includes dealing cards to stockpile and columns
        PrepareGame(self.cards,self.stockPile, self.tableauColumns, self.dictionary, self.LinkedList)

        # this function sets and creates labels according to  cards present data structures
        self.updateTableau()


        # these are used for selecting cards and eventually their movements
        self.firstSelected = None
        self.secondSelected = None

        # this is used to identify the present card of stockpile 
        self.currentStockCard = None
 

        # this label shows the user if they made a right move or not and explain the reason
        self.faultLabel = self.findChild(QLabel, "error")


        # this is the label of the clock which shows the time since user started playing the game
        self.clockLabel = self.findChild(QLabel, "clock")

        # this is the label for keeping track of the score and showing it
        self.scoreLabel = self.findChild(QLabel, "score")


        # these are used for identification and finding stockpile and wastepile and foundation pile labels from UI
        self.stockLabel = self.findChild(QLabel, "Stockpile")
        self.CardFromStock = self.findChild(QLabel, "CardFromStock")
        self.SpadesPile = self.findChild(QLabel, "spadesPile")
        self.HeartsPile = self.findChild(QLabel, "heartsPile")
        self.ClubsPile = self.findChild(QLabel, "clubsPile")
        self.DiamondsPile = self.findChild(QLabel, "diamondsPile")


        # this sets up their mouse click event which mainly calls check click function 
        self.stockLabel.mousePressEvent = lambda event: self.HandleStockPile() # this one handles the stockpile on clicking
        # thse handle the foundation piles and wastepile
        self.CardFromStock.mousePressEvent = lambda event: self.checkClick(self.CardFromStock)
        self.SpadesPile.mousePressEvent = lambda event: self.checkClick(self.SpadesPile)
        self.HeartsPile.mousePressEvent = lambda event: self.checkClick(self.HeartsPile)
        self.ClubsPile.mousePressEvent = lambda event: self.checkClick(self.ClubsPile)
        self.DiamondsPile.mousePressEvent = lambda event: self.checkClick(self.DiamondsPile)

        # this checks if the undo button exist and then calls its click event
        if self.undoButton is not None:
            self.undoButton.clicked.connect(self.manageUndo) # manage undo is the function which manages undo operation
        else:
            print("button not found")

        

        # this identifies the columns which are setup by the update tableau function
        self.initializeTableauLabels()

        # this is to show the ui to the user
        self.show()


    # this function identifies the label containing cards which are setup dynamically 
    def initializeTableauLabels(self):
        lastLabel = None
        for i in range(7):
            for cardNo in range(self.tableauColumns[i].getSize()+self.LinkedList[i].getSize()):  # this iterates for every card 
                label = self.findChild(QLabel, f"column{i+1}_label_{cardNo}") # the card in column as well as the linked list
                if label is not None:
                    print(f"Label column{i+1}_label_{cardNo} found!")
                    label.mousePressEvent = lambda event, lbl=label: self.checkClick(lbl) # it also sets up its mouse click event
                    lastLabel = label


    # this function updates the score label
    def updateScore(self):
        self.scoreLabel.setText(f"Score : {str(self.scoreObject.getScore())}")



    # starts the timer
    def startTimer(self):
        self.eTimer = QElapsedTimer()
        self.eTimer.start()
                

    # this function breaks the elapsed time in sec, min  and hours and then sets up clock label text
    def updateClock(self):
        time = self.eTimer.elapsed()
        seconds = (time//1000)%60
        mins = (time // (1000*60))%60
        hours = (time // (1000*60*60))%24
        timeString = f"{hours:02}:{mins:02}:{seconds:02}"
        self.clockLabel.setText(timeString)


    # this function which label were clicked and assigns them first or second turn depending on the order they were clicked
    def checkClick(self, label):

        if self.firstSelected is None:
            self.firstSelected = label
            giveBorder(self.firstSelected) # if it is selected then it assigns a border to it
        else:
            self.secondSelected = label
            giveBorder(self.secondSelected)
            removeBorder(self.firstSelected)
            self.tryingMovement(self.firstSelected, self.secondSelected) # if both the labels are identified it calls movement function where one is source and the other is destination
            self.firstSelected = None

        if self.secondSelected is not None:
            removeBorder(self.secondSelected) # if not selected remove border
            self.secondSelected = None


    # this function handles the complete movement of cards from one place to another depending upon the source and destination
    def tryingMovement(self, labelSource, labelDes): 
        count = 0

        # extract the source and destincation columns
        columnSource = extractColumn(labelSource.objectName())
        columnDes = extractColumn(labelDes.objectName())

        print("source column:" , columnSource)
        print("destination column:", columnDes)

        # if both selections are same then return
        if labelSource.objectName() == labelDes.objectName():
            self.deselectCards()
            return

        # if source is foundation and target is stockpile it is not possible
        if checkDestination(labelSource.objectName()) and labelDes.objectName() == "CardFromStock":
            print("cant move from foundation to stock")
            self.faultLabel.setText("can't move from foundation to stock")
            self.deselectCards()
            return
        
        # if source and destination are both in foundation then return
        if checkDestination(labelSource.objectName()) and checkDestination(labelDes.objectName()):
            self.faultLabel.setText("can't move from foundation to foundation")
            self.deselectCards()
            return

        # this is for the movement from stockpile to columns
        if labelSource.objectName() == "CardFromStock" and not checkDestination(labelDes.objectName()):
            card = self.currentStockCard # this selects the card from the stockpile
            if card is not None:
                cardDes = self.LinkedList[extractColumnNumber(columnDes)-1].peakLast() # this gets the last card from linked list of that column
                if self.checkValidMove(card, cardDes): # check if the movement is legal or not
                    self.moveFromStockToColumn(columnDes, card)
                    self.dictionary.AddtoTableauDict(f"column{extractColumnNumber(columnDes)}", card) # add to dictionary not used
                    self.takeReferencesForUndo(labelSource, labelDes) # this takes the ref for undo in the future
                    self.faultLabel.setText("")
                else:
                    self.deselectCards()
                    self.faultLabel.setText("not a valid move")

        # this is to move from foundation to columns
        elif checkDestination(labelSource.objectName()) and isColumnLabel(labelDes):
            stack = self.findFoundation(labelSource) # finds the foundation from which card is coming from
            if stack:
                print(stack.getSize())
            card = stack.peak()  # get the last card from its stack
            if card is not None:
                print(card.getCardDetail())
                cardDes = self.LinkedList[extractColumnNumber(columnDes)-1].peakLast()
                if self.checkValidMove(card, cardDes): # check the validity of the move
                    self.updateFoundationPile(stack, labelSource) 
                    self.moveFromFoundationToCol(columnDes, card, labelSource)
                    self.dictionary.RemoveFromFoundationDict(labelSource.objectName(), card)
                    self.dictionary.AddtoTableauDict(extractColumnNumber(columnDes),card)
                    self.scoreObject.removePoints(5) #this will remove points from the score
                    self.takeReferencesForUndo(labelSource, labelDes)

                else:
                    self.deselectCards()
            else:
                print("card is empty")


        # this is for the movement of card from either stockpile or columns to foundation pile of spade
        elif labelDes.objectName().lower() == "spadespile":
            if labelSource.objectName() == "CardFromStock": # this is for the case where source is from wastepile
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
                        self.faultLabel.setText("")
            else:
                card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast() # if card is coming from a column
                if card is not None:
                    if self.checkForSpadesFoundation(card): # make necessary changes
                        self.foundationSpades.push(card)
                        self.movefromColToFoundation(self.SpadesPile, columnSource, card)
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        labelSource.clear()
                        labelSource.hide()
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                        self.faultLabel.setText("")
                    else:
                        print("card not according to spade foundation criteria")
                        self.faultLabel.setText("card not according to spades foundation criteria")


        # this is for the movement of card from either stockpile or columns to foundation pile of hearts
        elif labelDes.objectName().lower() == "heartspile":
            if labelSource.objectName() == "CardFromStock": # case where source is wastepile
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
                        self.faultLabel.setText("")
            else:
                card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast() # case where source is column
                if card is not None:
                    if self.checkForHeartsFoundation(card): # make necessary changes
                        self.foundationHearts.push(card)
                        self.movefromColToFoundation(self.HeartsPile, columnSource, card)
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        labelSource.clear()
                        labelSource.hide()
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                        self.faultLabel.setText("")
                    else:
                        print("card not according to hearts foundation criteria")
                        self.faultLabel.setText("card not according to hearts foundation criteria")


        # this is for the movement of card from either stockpile or columns to foundation pile of clubs
        elif labelDes.objectName().lower() == "clubspile":
            if labelSource.objectName() == "CardFromStock": # first case card from wastepile
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
                        self.faultLabel.setText("")
            else:
                card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast() # card from columns
                if card is not None:
                    if self.checkForClubsFoundation(card):
                        self.foundationClubs.push(card)
                        self.movefromColToFoundation(self.ClubsPile, columnSource, card)
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        labelSource.clear()
                        labelSource.hide()
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                        self.faultLabel.setText("")
                    else:
                        print("card not according to clubs foundation criteria")
                        self.faultLabel.setText("card not according to clubs foundation criteria")



        # this is for the movement of card from either stockpile or columns to foundation pile of diamonds
        elif labelDes.objectName().lower() == "diamondspile":
            if labelSource.objectName() == "CardFromStock":
                card = self.currentStockCard # card from stockpile or wastepule
                if card is not None:
                    if self.checkForDiamondsFoundation(card):
                        self.foundationDiamonds.push(card)
                        manageStateOfCard(card, self.dictionary, True)
                        self.HandleWastePile()
                        setImage(self.DiamondsPile, card.getCardImage())
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                        self.faultLabel.setText("")
            else:
                card = self.LinkedList[extractColumnNumber(columnSource)-1].peakLast() # card came from colummsn
                if card is not None:
                    if self.checkForDiamondsFoundation(card):
                        self.foundationDiamonds.push(card)
                        self.movefromColToFoundation(self.DiamondsPile, columnSource, card)
                        self.dictionary.AddToFoundationDict(labelDes.objectName(), card)
                        labelSource.clear()
                        labelSource.hide()
                        self.scoreObject.addPoints(10)
                        self.takeReferencesForUndo(labelSource, labelDes)
                        self.faultLabel.setText("")
                    else:
                        print("card not according to diamonds foundation criteria")
                        self.faultLabel.setText("card not according to diamond foundation criteria")


        # this is for movement of cards or cards between columns
        elif checkForColToCol(labelSource, labelDes):
            
            columnNumber = extractColumnNumber(columnSource)
            index = self.calculateIndexOfList(labelSource) # get the indedx at which card is removed from source column
            node = self.LinkedList[columnNumber-1].returnNodeAtIndex(index)  # this gets the reference of the node at that index
             
            if node is not None:
                print(node.card.getCardDetail())
                cardDes = self.LinkedList[extractColumnNumber(columnDes)-1].peakLast() # get the last card of destination column
                if self.checkValidMove(node.card, cardDes):
                    count = self.AddCardsInColumnList(extractColumnNumber(columnDes)-1, node)
                    current = node
                    # this is done only to maintain dictionary which is not used
                    while current is not None:
                        self.dictionary.AddtoTableauDict(extractColumnNumber(columnDes), current.card)
                        self.dictionary.RemoveFromTableauDict(columnNumber, current.card)
                        current = current.next
                    
                    self.takeReferencesForUndo(labelSource, labelDes)
                    self.scoreObject.addPoints(5)
                else:
                    current = node
                    while current is not None:
                        # again only for dictionary which is not used
                        self.dictionary.AddtoTableauDict(extractColumnNumber(columnDes), current.card)
                        self.dictionary.RemoveFromTableauDict(columnNumber, current.card)
                        current = current.next

                    # as cards are popped then it will return to source column
                    self.AddCardsInColumnList(columnNumber-1, node)
                    self.deselectCards()
            else:
                print("node is empty")




        # this is to check if source is a column and if needs to pop a card
        if isColumnLabel(labelSource):
            if self.LinkedList[extractColumnNumber(columnSource)-1].getSize() == 0:
                self.moveCardFromStackToList(extractColumnNumber(columnSource)-1)

                
            # this is done to calucalte the number of what needs to clear the ui labels
            columnNumber = int(labelSource.objectName().split('_')[0][6])  
            labelNumber = int(labelSource.objectName().split('_')[2])
            self.clearRemLabels(labelNumber, count+labelNumber, columnNumber)
                
            

        # these are called everytime movement is called
        self.updateTableau()
        self.initializeTableauLabels()
        self.updateScore()

        # this is to check the win condition
        self.checkWinCondition()

    def clicker(self, sen):
        print(sen)


    # this function creates the labels 
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

            # get the geometry of the first card in the column

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

            # after completing cards of the tableau it moves to the linked list
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
                    
                else:
                    print("wasnt there")

                # moves to the next node with every iteration
                currentNode = currentNode.next
                k=k+1

            #this is done for ui to not lose reference of the first card if it is empty
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



    # this functions is called for the movement of the card from column to foundation pile
    def movefromColToFoundation(self, label, columnSource, card):
        setImage(label, card.getCardImage())
        card = self.LinkedList[extractColumnNumber(columnSource)-1].removeCardFromLast()
        print(card.getCardDetail())
        self.dictionary.RemoveFromTableauDict(f"column{columnSource}", card)

    # this is called to move from stockpile(wastepile) to list of the column 
    def moveCardFromStackToList(self, column):
        if not self.tableauColumns[column].isEmpty():
            card = self.tableauColumns[column].pop()
            self.AddCardInColumnList(column, card)
            self.dictionary.AddtoTableauDict(f"column{column+1}", card)
            self.scoreObject.addPoints(10)

    # this calculates the index at which the node will be removed from linked list while movement

    def calculateIndexOfList(self, label):
        columnNumber = int(label.objectName().split('_')[0][6])  
        labelNumber = int(label.objectName().split('_')[2])
        print("columNumber", columnNumber)
        print("labelNumber", labelNumber)
        index = labelNumber - self.tableauColumns[columnNumber-1].getSize()
        print(index)
        return index

    
    # this function sets up reference for the undo operation
    def takeReferencesForUndo(self, labelSource, labelDes):
        self.sourceLabel = labelDes
        self.destinationLabel = labelSource

    # this function handles the undo operation from column to any of the foundation pile
    def undoFromColumnToFoundation(self):
        self.tryingMovement(self.sourceLabel, self.destinationLabel)
        self.scoreObject.removePoints(20)


    # this handles the movement undo of the card from a column back to the stockpile
    def undoFromColumnToStock(self):
        columnNumberOfDes = extractColumnNumber(extractColumn(self.sourceLabel.objectName()))-1
        card = self.LinkedList[columnNumberOfDes].removeCardFromLast()
        self.wastePile.push(card)
        self.currentStockCard = self.wastePile.peak()
        self.updateWastePileForUndo()

        totalSize = self.tableauColumns[columnNumberOfDes].getSize() + self.LinkedList[columnNumberOfDes].getSize()



        # this is to clear unwanted label and end their reference
        self.sourceLabel.clear()
        self.sourceLabel.hide()
        self.scoreObject.removePoints(20)
        self.sourceLabel = None
        self.destinationLabel = None


        self.updateScore()
        self.updateTableau()
        self.initializeTableauLabels()


    # this function manages the undo operation depending on the source and destinaions
    def manageUndo(self):
        if self.sourceLabel is not None and self.destinationLabel is not None: # if both labels are none the undo functionality is empty
            self.faultLabel.setText("")
            print(self.sourceLabel.objectName())
            print(self.destinationLabel.objectName())

            # if the undo is being done from column to foundation pile
            if isColumnLabel(self.sourceLabel) and checkDestination(self.destinationLabel.objectName()):

                self.undoFromColumnToFoundation()

            # if the undo is done from a foundation pile
            elif checkDestination(self.sourceLabel.objectName()):
                    # if the destination is wastepile
                if self.destinationLabel.objectName() == "CardFromStock":
                    self.undoFromFoundationToStock()
                else:
                    # if the destination is a column
                    self.sourceLabel = self.findChild(QLabel, extractColumn(self.sourceLabel.objectName())) 
                    self.undoFromFoundationToColumn()

            # this is for the case where card is coming from column back to the stockpile
            elif self.destinationLabel.objectName() == "CardFromStock":
                 self.undoFromColumnToStock()
                
            # this is for the case where there is undo between movement of columns card
            elif isColumnLabel(self.sourceLabel) and isColumnLabel(self.destinationLabel):
                self.undoFromColToCol()

            else:
                print("couldnt find")


            # lost the reference of both the labels so there is no undo more than once
            self.sourceLabel = None
            self.destinationLabel = None
        else:
            print("nothing to undo")
            self.faultLabel.setText("Nothing to Undo")


    # this is called for the case where undo is done between columns
    def undoFromColToCol(self):
        
        count = 0
        columnNumberOfDes = extractColumnNumber(extractColumn(self.destinationLabel.objectName()))-1
        columnNumberOfSource = extractColumnNumber(extractColumn(self.sourceLabel.objectName()))-1

        # if the linked list of the destination is greater than 1 or less than 1 mean empty (there is no popping from the tableau column)
        if self.LinkedList[columnNumberOfDes].getSize() > 1 or self.LinkedList[columnNumberOfDes].getSize() < 1:
            index = self.calculateIndexOfList(self.sourceLabel)
            node = self.LinkedList[columnNumberOfSource].returnNodeAtIndex(index+1)
            if node is not None:
                print(node.card.getCardDetail())
                count = self.AddCardsInColumnList(columnNumberOfDes, node)
                self.scoreObject.removePoints(20)
            else:
                print("nonenenene")

        # if the linked list pf the destination is one means there was popping after movenment 
        elif self.LinkedList[columnNumberOfDes].getSize() == 1:
            card = self.LinkedList[columnNumberOfDes].removeCardFromLast()
            self.tableauColumns[columnNumberOfDes].push(card)
            print(self.sourceLabel.objectName())
            index = self.calculateIndexOfList(self.sourceLabel)
            node = self.LinkedList[columnNumberOfSource].returnNodeAtIndex(index+1)
            if node is not None:
                print(node.card.getCardDetail())
                count = self.AddCardsInColumnList(columnNumberOfDes, node)
                self.scoreObject.removePoints(20)
            else:
                print("nonenenene")

        # this is to remove unwanted labels from the ui
        columnNumber = int(self.sourceLabel.objectName().split('_')[0][6])  
        labelNumber = int(self.sourceLabel.objectName().split('_')[2])
        self.clearRemLabels(labelNumber, count+labelNumber, columnNumber)
        self.updateTableau()
        self.initializeTableauLabels()

            

    # this si to apply the foundation to stock undo movement
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

    # this is to undo from foudaation to columns
    def undoFromFoundationToColumn(self):
        columnNumberOfDes = extractColumnNumber(extractColumn(self.destinationLabel.objectName()))-1

        # if linked list is greater than 1 ot less than 1 (no popping in movement)
        if self.LinkedList[columnNumberOfDes].getSize() > 1 or self.LinkedList[columnNumberOfDes].getSize() < 1:
            self.tryingMovement(self.sourceLabel, self.destinationLabel)
            self.scoreObject.removePoints(20)

        # if there was popping of tableau in movement before hand
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

    # this is for the movemetn of card from stockpile to column
    def moveFromStockToColumn(self, columnDes, card):
        self.AddCardInColumnList(extractColumnNumber(columnDes)-1, card)
        self.HandleWastePile()
        self.dictionary.AddtoTableauDict(f"column{columnDes}", card)

    # this for the movement of card from foundation to column
    def moveFromFoundationToCol(self, columnDes, card, label):
        self.AddCardInColumnList(extractColumnNumber(columnDes)-1, card)
        self.dictionary.AddtoTableauDict(f"column{columnDes}", card)

    # this function is used to add card in the linked lsit of a given column
    def AddCardInColumnList(self, columnNumber, card):

        if card is not None:  # Ensure that card is not None
            self.LinkedList[columnNumber].AddCard(card)
            print(f"Card {card.getCardDetail()} added to column {columnNumber + 1}")
            
        else:
            print("Cannot add empty card to linked list")

    # this is used to add more than one card in linked list of column
    def AddCardsInColumnList(self, columnNumber, node):

        count = 0
        if node is not None:  # Ensure that card is not None
           count =  self.LinkedList[columnNumber].AddCards(node)
        else:
            print("Cannot add empty nodd to linked list")
        
        return count

    # this is to remove the last card from a column
    def removeCardLast(self, columnNumber):
        if not self.LinkedList[columnNumber].isEmpty():
            card = self.LinkedList[columnNumber].removeCardFromLast()
            print(f"Removed card {card.getCardDetail()} from column {columnNumber + 1}")
            return card

        else:
            print("Cannot remove from empty list")
            return None


    # this function handles the stockpile and updates its ui
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

    # this is used to peak the top card of waste
    def peakFromWaste(self):
        return self.wastePile.peak()


    # this is to update the ui of the foundation pile
    def updateFoundationPile(self, stack, label):
        stack.pop()
        card = stack.peak()
        if card is not None:
            manageStateOfCard(card, self.dictionary, True)
            setImage(label, card.getCardImage())
        else: 
            removeImage(label)

    # this is used to find the correct foundationpile based on label
        
    def findFoundation(self, label):
        if label.objectName().lower() == "spadespile":
            return self.foundationSpades
        elif label.objectName().lower() == "heartspile":
            return self.foundationHearts
        elif label.objectName().lower() == "diamondspile":
            return self.foundationDiamonds
        elif label.objectName().lower() == "clubspile":
            return self.foundationClubs

    # this function handle the wastepile and updates it ui

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


    # this function checks a move is valid or not
    def checkValidMove(self,card1, card2):
        if card2 is None:
            #means moving card to empty column
            return True

        # gets appropriate rank from dictionary and then comapares
        if self.dictionary.getRank(card1.rank) != self.dictionary.getRank(card2.rank)-1:
            print(card1.getCardDetail())
            print(card2.getCardDetail())
            print("not valid", card1.rank, "  ", card2.rank)
            self.faultLabel.setText("Not a valid Move")
            return False

        # after checking rank it check the colour or suit which is also from dictionary and then compared
        if self.dictionary.colourMap[card1.suit.lower()] == self.dictionary.colourMap[card2.suit.lower()]:
            print("not valid", card1.suit, "  ", card2.suit)
            self.faultLabel.setText("Not a valid Move")
            return False

        # if both cases are not false return true
        self.faultLabel.setText("")
        return True


    # this is to check if the card should be a part of the spades foundation
    def checkForSpadesFoundation(self, card):
        lastCard = self.foundationSpades.peak()
        if lastCard is not None:
            if card.suit.lower() == "spades" and self.dictionary.getRank(card.rank) == self.dictionary.getRank(lastCard.rank)+1:
                self.faultLabel.setText("")
                return True
        elif lastCard is None:
            if card.suit.lower() == "spades" and self.dictionary.getRank(card.rank) == 1:
                self.faultLabel.setText("")
                return True
        else:
            self.faultLabel.setText("Not valid")
            return False



# this is to check if the card should be a part of the hearts foundation
    def checkForHeartsFoundation(self, card):
        lastCard = self.foundationHearts.peak()
        if lastCard is not None:
            if card.suit.lower() == "hearts" and self.dictionary.getRank(card.rank) == self.dictionary.getRank(lastCard.rank)+1:
                self.faultLabel.setText("")
                return True
        elif lastCard is None:
            if card.suit.lower() == "hearts" and self.dictionary.getRank(card.rank) == 1:
                self.faultLabel.setText("")
                return True
        else:
            self.faultLabel.setText("not valid")
            return False


# this is to check if the card should be a part of the clubs foundation
    def checkForClubsFoundation(self, card):
        lastCard = self.foundationClubs.peak()
        if lastCard is not None:
            if card.suit.lower() == "clubs" and self.dictionary.getRank(card.rank) == self.dictionary.getRank(lastCard.rank)+1:
                self.faultLabel.setText("")
                return True
        elif lastCard is None:
            if card.suit.lower() == "clubs" and self.dictionary.getRank(card.rank) == 1:
                self.faultLabel.setText("")
                return True
        else:
            self.faultLabel.setText("not valid")
            return False



# this is to check if the card should be a part of the diamonds foundation
    def checkForDiamondsFoundation(self, card):
        lastCard = self.foundationDiamonds.peak()

        if lastCard is not None:
            if card.suit.lower() == "diamonds" and self.dictionary.getRank(card.rank) == self.dictionary.getRank(lastCard.rank)+1:
                self.faultLabel.setText("")
                return True
        elif lastCard is None:
            if card.suit.lower() == "diamonds" and self.dictionary.getRank(card.rank) == 1:
                self.faultLabel.setText("")
                return True
        else:
            self.faultLabel.setText("not valid")
            return False


    # this is to clear the unwanted labels in ui
    def clearRemLabels(self,start, end, column):
        for i in range(start, end+13):
            label = self.findChild(QLabel, f"column{column}_label_{i}")
            if label is not None:
                label.clear()
                label.hide()

    # specailly hanldes the wastepile for the undo procedure
    def updateWastePileForUndo(self):
        card = self.wastePile.peak()
        
        if card is not None:
            manageStateOfCard(card, self.dictionary, True)
            setImage(self.CardFromStock, card.getCardImage())
            self.currentStockCard = card
        else: 
            removeImage(self.CardFromStock)
            self.currentStockCard = None


    # this is to deselect selected cards
    def deselectCards(self):
        removeBorder(self.firstSelected)
        self.firstSelected = None
        removeBorder(self.secondSelected)
        self.secondSelected = None

# this functions checks if the destination is any of the foundation piles
def checkDestination(sen):
    array = ["spadespile", "heartspile", "clubspile", "diamondspile"]
    if sen.lower() in array:
        return True
    return False

# this function pushes the card in wastepile dequeued from stockpile
def handleDequeue(stockPile, wastePile):
    card = stockPile.dequeue()
    if card:
        wastePile.push(card)
    return card

# if bothe source and destination label reference a column
def checkForColToCol(labelSource, labelDes):
    if isColumnLabel(labelSource) and isColumnLabel(labelDes):
        print("condition was true")
        return True
    print("condition was false")
    return False


# this is also check if the label reference a column
def isColumnLabel(label):
    return label.objectName()[:6] == "column"


# this is to manage state of a card in the dictionary
def manageStateOfCard(card, dictionary, faceUp):
    dictionary.changeState(card, faceUp)

        
# this is called if stockpile is empty
def requeueCards(stockPile, wastePile):
    cards = []
    while not wastePile.isEmpty():
        cards.append(wastePile.pop())
    
    cards = ShuffleCards(cards)
    stockPile.reQueue(cards)

# this functions get the column name from label
def extractColumn(sen):
    return sen.split('_')[0]

# this functions extracts the column number from colmn name
def extractColumnNumber(sen):
    return int(sen[6])

# this sets image to a label
def setImage(label, imageAddress):
    pixmap = QPixmap(imageAddress)
    label.setPixmap(pixmap)
    label.setScaledContents(True)

# this remove image
def removeImage(label):
    label.clear()

# this function gives address to the back of a card
def giveBackImage():
    return f"SuitsImages/back.jpeg"



def giveBorder(label):
    label.setStyleSheet("border: 2px solid black; padding: 5px;")
    label.update()

def removeBorder(label):
    if label is not None:
        label.setStyleSheet("")
        label.update()

 


# this function sets up the game by dealing cards first to tableau then to linked list and then to stockpile
def PrepareGame(cards, stockPile, tableauColumns, dictionary, LinkedList):

    #prepare the tableau columns
    if cards: 
        for i in range(7):
            tempStack = []
            for j in range(i+1):
                card = cards.pop(0)
                if j == i: # if it is the last index add in linked list
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