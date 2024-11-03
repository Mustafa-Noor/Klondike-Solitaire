from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QMouseEvent
from PyQt5.QtCore import Qt, QMimeData, QPoint

class DraggableCard(QLabel):
    def __init__(self, card_text, parent=None):
        super().__init__(card_text, parent)
        self.setPixmap(QPixmap(100, 150))  # Sample size for the card
        self.setStyleSheet("border: 1px solid black; background-color: white;")
        self.setAlignment(Qt.AlignCenter)
        self.card_text = card_text

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()  # Record start position for drag
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and \
           (event.pos() - self.drag_start_position).manhattanLength() >= QApplication.startDragDistance():
            self.startDrag()
            event.accept()

    def startDrag(self):
        # Create drag object with mimedata to represent the dragged card
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.card_text)  # Pass the card's information
        drag.setMimeData(mime_data)

        # Set a pixmap to show a "ghost" of the card during the drag
        pixmap = self.grab()  # Grab the current widget appearance
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))  # Set cursor in the center of the pixmap

        drag.exec_(Qt.MoveAction)  # Execute drag with move action

class DropArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: lightgreen; border: 2px dashed black;")
        self.setFixedSize(120, 180)  # Sample size for the drop area

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        card_text = event.mimeData().text()
        self.setWindowTitle(f"Dropped card: {card_text}")  # Example of drop action
        event.acceptProposedAction()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Card Example")

        # Create draggable card
        self.card = DraggableCard("Ace of Spades", self)
        self.card.move(50, 50)

        # Create drop area
        self.drop_area = DropArea(self)
        self.drop_area.move(200, 50)

        # Set the window size
        self.setGeometry(300, 300, 400, 300)

# Run the PyQt application
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
