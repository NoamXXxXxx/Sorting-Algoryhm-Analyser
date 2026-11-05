import sys
from PyQt6.QtWidgets import QApplication
from ui import AlgoAnalyzerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AlgoAnalyzerApp()
    window.show()
    sys.exit(app.exec())