from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import Qt, QRect

class PenduWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 300)
        self.errors = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))
        width = self.width()
        height = self.height()

        # Coordonnées de référence pour dessiner le pendu
        start_x = width / 2
        start_y = height / 2

        # Dessiner le pendu en fonction du nombre d'erreurs
        if self.errors >= 1:
            # Poteau vertical
            painter.drawLine(start_x, start_y +100, start_x, start_y - 100)
        if self.errors >= 2:
            # Poutre horizontale
            painter.drawLine(start_x, start_y - 100, start_x - 50, start_y - 100)
        if self.errors >= 3:
            # Corde
            painter.drawLine(start_x - 50, start_y - 100, start_x - 50, start_y - 80)
        if self.errors >= 4:
            # Tête
            radius = 20
            head_center = QRect(start_x -50 - radius, start_y - 80, radius * 2, radius * 2)
            painter.drawEllipse(head_center)
        if self.errors >= 5:
            # Corps
            painter.drawLine(start_x-50, start_y - 40, start_x-50, start_y + 40)
        if self.errors >= 6:
            # Bras gauche
            painter.drawLine(start_x-50, start_y -20, start_x - 80, start_y)
        if self.errors >= 7:
            # Bras droit
            painter.drawLine(start_x-50, start_y -20, start_x - 20, start_y)
        if self.errors >= 8:
            # Jambe gauche
            painter.drawLine(start_x-50, start_y + 40, start_x - 80, start_y + 100)
        if self.errors >= 9:
            # Jambe droite
            painter.drawLine(start_x-50, start_y + 40, start_x -20, start_y + 100)

    def setError(self):
        self.errors += 1
        self.update()
