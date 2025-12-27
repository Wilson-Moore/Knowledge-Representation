from PyQt5.QtWidgets import QApplication, QStackedWidget
import sys

from .components.welcome import WelcomePage
from .components.patient_info import PatientPage
from .components.symptoms import SymptomsPage
from .components.res import ResultPage

class MedicalApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        
        self.welcome_page = WelcomePage(self)
        self.patient_page = PatientPage(self)
        self.symptoms_page = SymptomsPage(self)
        self.result_page = ResultPage(self)
        
        self.addWidget(self.welcome_page)
        self.addWidget(self.patient_page)
        self.addWidget(self.symptoms_page)
        self.addWidget(self.result_page)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MedicalApp()
    window.setWindowTitle("Medical Diagnosis Assistant")
    window.resize(600, 600)
    window.show()
    sys.exit(app.exec())