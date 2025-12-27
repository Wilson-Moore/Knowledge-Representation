from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from ..Helpers.Menu_icon import MenuIcon

class Navbar(QWidget):
    def __init__(self, stack, parent=None):
        super().__init__(parent)
        self.stack = stack

        self.logo = QLabel("LungCare")
        self.logo.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel:hover {
                color: #3498db;
            }
        """)
        self.logo.setAlignment(Qt.AlignLeft)
        self.logo.setCursor(Qt.PointingHandCursor)
        self.logo.mousePressEvent = self.go_home

        self.menu_icon = MenuIcon(self.stack)

        layout = QHBoxLayout()
        layout.addWidget(self.logo)
        layout.addStretch()
        layout.addWidget(self.menu_icon)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def go_home(self, event):
        self.stack.setCurrentIndex(0)
