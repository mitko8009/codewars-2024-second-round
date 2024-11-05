from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys

from init import *
import database
import utils

# Window class
# This class is responsible for GUI and functionality of the application
class window(QMainWindow):
    def __init__(self):
        app = QApplication(sys.argv)
        super(window, self).__init__()
        initConfig()
        
        self.mainUi = uic.loadUi(utils.resource_path("ui/main.ui"), self)
        self.mainUi.setWindowTitle(config["title"])
        self.mainUi.setWindowIcon(QIcon(utils.resource_path("assets/icon.png")))
        
        self.functionality()
        
        self.mainUi.show()
        sys.exit(app.exec_())
        
        
    def functionality(self):
        data = database.get_all_urls()
        for i in data:
            self.addUrlToTable(i.url, i.shortcode)
        
        self.mainUi.shorturl_edit.setEnabled(False)
        self.mainUi.custom_shortcode.clicked.connect(self.customShortcode)
        
        self.mainUi.AddButton.clicked.connect(self.addUrl)
        
    
    def addUrlToTable(self, url, shortcode):
        table = self.mainUi.DataTable
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, QTableWidgetItem(url))
        table.setItem(rowPosition, 1, QTableWidgetItem(shortcode))
        table.setItem(rowPosition, 2, QTableWidgetItem(f"http://localhost:5000/{shortcode}"))
        
        
    def addUrl(self):
        url = self.mainUi.longurl_edit.text()
        if not url:
            return
        
        if self.isCustomShortCode() and self.mainUi.shorturl_edit.text() != "":
            shortcode = self.mainUi.shorturl_edit.text()
            self.mainUi.shorturl_edit.setText("")
        else:
            shortcode = database.generate_unique_shortcode()
        
        if database.shortcode_exists(shortcode):
            self.mainUi.shorturl_edit.setPlaceholderText("Shortcode already exists")
            return
        
        if len(shortcode) < config['min_short_url_length']:
            self.mainUi.shorturl_edit.setPlaceholderText("Shortcode must be at least 3 characters long")
            return
        
        if len(shortcode) > config['max_short_url_length']:
            self.mainUi.shorturl_edit.setPlaceholderText("Shortcode must be at most 20 characters long")
            return
        
        database.insert_url(url, shortcode)
        self.addUrlToTable(url, shortcode)
        self.mainUi.shorturl_edit.setPlaceholderText("Shortcode")
        self.mainUi.longurl_edit.setText("")
        
    # Check if the user wants to use custom shortcode
    def isCustomShortCode(self) -> bool:
        return self.mainUi.custom_shortcode.checkState() == 2 and True or False
    
        
    def customShortcode(self):
        if self.isCustomShortCode():
            self.mainUi.shorturl_edit.setEnabled(True)
        else:
            self.mainUi.shorturl_edit.setEnabled(False)

if __name__ == "__main__":
    window()
