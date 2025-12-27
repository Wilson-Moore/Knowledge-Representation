from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QMenu
from PyQt5.QtCore import Qt, QPoint

class MenuIcon(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        grid = QGridLayout()
        grid.setSpacing(3)
        grid.setContentsMargins(0, 0, 0, 0)

        for row in range(3):
            for col in range(3):
                box = QLabel()
                box.setFixedSize(6, 6)
                box.setStyleSheet("""
                    background-color: #2c3e50;
                    border-radius: 50px;
                """)
                grid.addWidget(box, row, col)

    
        self.setLayout(grid)
        self.setFixedSize(30, 30)
        self.setCursor(Qt.PointingHandCursor)

        self.create_menu()

    def create_menu(self):
        self.menu = QMenu(self)

        self.menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #dcdcdc;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                color: #2c3e50;
            }
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

        home_action = self.menu.addAction("Home")
        new_action = self.menu.addAction("New Diagnosis")
        about_action = self.menu.addAction("About")
        self.menu.addSeparator()
        exit_action = self.menu.addAction("Exit")

        home_action.triggered.connect(lambda: self.go_to(0))
        new_action.triggered.connect(lambda: self.go_to(1))
        # about_action.triggered.connect(lambda: self.go_to(2))
        exit_action.triggered.connect(self.close_app)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.menu.exec_(self.mapToGlobal(QPoint(0, self.height())))
    def go_to(self, index):
        if self.stack:
            self.stack.setCurrentIndex(index)

    def close_app(self):
        self.window().close()
