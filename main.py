from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os

from init import *
from database import *
import utils

class window(QMainWindow):
    def __init__(self):
        app = QApplication(sys.argv)
        super(window, self).__init__()
        initConfig()
        
        self.mainUi = uic.loadUi("main.ui", self)
        self.mainUi.setWindowTitle(config["title"])
        self.mainUi.setWindowIcon(QIcon("icon.png"))
        
        self.functionality()
        
        self.mainUi.show()
        sys.exit(app.exec_())
        
    def functionality(self):
        data = get_all_urls()
        for i in data:
            self.addUrlToTable(i.url, i.shortcode)
    
    def addUrlToTable(self, url, shortcode):
        table = self.mainUi.DataTable
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, QTableWidgetItem(url))
        table.setItem(rowPosition, 1, QTableWidgetItem(shortcode))
        table.setItem(rowPosition, 2, QTableWidgetItem(f"http://localhost:5000/{shortcode}"))

if __name__ == "__main__":
    window()
