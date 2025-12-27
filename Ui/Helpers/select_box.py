from PyQt5.QtWidgets import QComboBox

class MultiSelectComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText("Select symptoms")

    def hidePopup(self):
        if self.view().underMouse():
            return
        super().hidePopup()
