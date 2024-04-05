import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    """
    TODO DEV-PRIOR: design user interface
    TODO DEV-PRIOR: MainWindow class
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Production Calculator")
