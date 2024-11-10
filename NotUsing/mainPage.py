import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5 import uic

class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        uic.loadUi('mainPage.ui', self)

        self.setStyleSheet("background-image: url('SuitsImages\wallpaper.webp');"
                           "background-repeat: no-repeat;"
                           "background-position: center;"
                           "background-size: cover;")
        
        self.startButton = self.findChild(QPushButton, 'startButton')
        self.startButton.clicked.connect(self.openGamePage)

    def openGamePage(self):
        self.gamePage = GamePage()
        self.gamePage.show()
        self.close()

class GamePage(QMainWindow):
    def __init__(self):
        super(GamePage, self).__init__()
        uic.loadUi('SolitaireUI.ui', self)

def main():
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
