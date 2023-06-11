from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import Qt, QRect
from mot import Mot
from pendu import PenduWidget
import logging

logging.basicConfig(filename='journal.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeu du Pendu")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.setup_default_values()
        self.setup_css()
        self.setup_connections()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.letter_layout = QHBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.lab_titre = QLabel()
        self.pendu_widget = PenduWidget()
        self.lab_sentence = QLabel()
        self.le_letter = QLineEdit()
        self.btn_try = QPushButton("Essayer cette lettre")

        self.layout.addWidget(self.lab_titre)
        self.layout.addWidget(self.pendu_widget)
        self.layout.addWidget(self.lab_sentence)
        self.layout.addLayout(self.letter_layout)
        self.layout.addLayout(self.btn_layout)

        self.spacer_left = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.letter_layout.addItem(self.spacer_left)
        self.letter_layout.addWidget(self.le_letter)
        self.spacer_right = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.letter_layout.addItem(self.spacer_right)

        self.btn_layout.addItem(self.spacer_left)
        self.btn_layout.addWidget(self.btn_try)
        self.btn_layout.addItem(self.spacer_right)

        self.setLayout(self.layout)

    def setup_default_values(self):
        self.lab_titre.setText("LE JEU DU PENDU")
        self.lab_sentence.setText(' '.join(m.finded_letter))
        self.le_letter.setMaxLength(1)

    def setup_css(self):
        self.setStyleSheet("""
        background: white;
        color: black;
        """)
        self.lab_titre.setStyleSheet("""
        font-size: 35px;
        font-weight: 700;
        """)
        self.lab_sentence.setStyleSheet("""
        font-size: 28px;
        font-weight: 500;
        letter-spacing: 6px;
        """)
        self.le_letter.setStyleSheet("""
        text-align: center;
        border: none;
        background: rgb(30,30,30);
        color: white;
        border-radius: 10px;
        padding: 5px;
        """)
        self.btn_try.setStyleSheet("""
        text-align: center;
        border: none;
        background: rgb(30,30,30);
        color: white;
        border-radius: 10px;
        font-size: 16px;
        """)

        font = QFont()
        font.setPointSize(30)
        font_btn = QFont()
        font.setPointSize(24)

        self.lab_titre.setAlignment(Qt.AlignCenter)
        self.lab_sentence.setAlignment(Qt.AlignCenter)
        self.le_letter.setFixedSize(35,35)
        self.le_letter.setFont(font)
        self.btn_try.setFixedSize(150, 50)
        self.btn_try.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_try.setFont(font_btn)

    def setup_connections(self):
        self.btn_try.clicked.connect(self.try_letter)
        self.le_letter.returnPressed.connect(self.try_letter)

    def try_letter(self):
        letter = self.le_letter.text().upper()
        if letter:
            if m._try_letter(letter):
                self.lab_sentence.setText(' '.join(m.finded_letter))
            else:
                self.pendu_widget.setError()
        self.le_letter.setText("")
        self._check_game()
    
    def _check_game(self):
        if self.pendu_widget.errors >= 9:
            self.loose_game()
        elif not '_' in m.finded_letter:
            self.win_game()
        else:
            return

    def loose_game(self):
        self.lab_titre.setText("PERDU")
        self.lab_titre.setStyleSheet("""
        font-size: 35px;
        font-weight: 700;
        color: crimson;
        """)
        self._reboot_btn()
        m._show_word()
        self.lab_sentence.setText(' '.join(m.finded_letter))
       
    def win_game(self):
        self.lab_titre.setText("GAGNÉ")
        self.lab_titre.setStyleSheet("""
        font-size: 35px;
        font-weight: 700;
        color: green;
        """)
        self._reboot_btn()

    def _reboot_btn(self):
        self.btn_try.setText("↻")
        self.btn_try.clicked.connect(self.reboot)
        try:
            self.btn_try.clicked.disconnect(self.try_letter)
            self.le_letter.returnPressed.disconnect(self.try_letter)
        except RuntimeError:
            logging.info("Le Line_Edit n'était pas connecter")

    def reboot(self):
        global m
        m = Mot()
        self.btn_try.clicked.disconnect(self.reboot)
        self.pendu_widget.errors = 0
        self.pendu_widget.update()
        self.btn_try.setText("Essayer cette lettre")
        self.setup_default_values()
        self.setup_css()
        self.setup_connections()


m = Mot()
app = QApplication([])
win = App()
win.show()
app.exec()