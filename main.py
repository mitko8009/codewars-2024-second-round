from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import threading
import sys

from init import *
import database
import router
import utils

# Window class
# This class is responsible for GUI and functionality of the application
class window(QMainWindow):
    def __init__(self):
        app = QApplication(sys.argv)
        super(window, self).__init__()
        initConfig()
        
        # Start the router server in a separate thread
        threading.Thread(target=router.run_server).start()
                
        self.mainUi = uic.loadUi(utils.resource_path("ui/main.ui"), self)
        self.mainUi.setWindowTitle(config["title"])
        self.mainUi.setWindowIcon(QIcon(utils.resource_path("assets/icon.png")))
        
        self.settingsUi = uic.loadUi(utils.resource_path("ui/settings.ui"))
        self.settingsUi.setWindowTitle("Settings")
        self.settingsUi.setWindowIcon(QIcon(utils.resource_path("assets/icon.png")))
        self.settingsUi.setParent(self.mainUi)
        self.settingsUi.setWindowFlags(Qt.WindowFlags(Qt.Dialog))
        
        self.functionality()
        
        self.mainUi.show()
        sys.exit(app.exec_())

     
    def functionality(self):
        data = database.get_all_urls()
        for i in data:
            self.addUrlToTable(i.url, i.shortcode)
        
        self.mainUi.shorturl_edit.setReadOnly(True)
        self.mainUi.custom_shortcode.clicked.connect(self.customShortcode)
        
        # Button actions
        self.mainUi.AddButton.clicked.connect(self.addUrl)
        self.mainUi.clearBtn.clicked.connect(self.clearfields)
        self.mainUi.deleteBtn.hide()
        self.mainUi.deleteBtn.clicked.connect(self.deleteSelectedUrl)
        
        # Table actions
        self.mainUi.DataTable.cellClicked.connect(self.cellClicked)
        
        # Menu actions
        self.mainUi.actionSettings.triggered.connect(self.settings)
        
    
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
            self.mainUi.shorturl_edit.setPlaceholderText(f"Shortcode must be at least {config['min_short_url_length']} characters long")
            return
        
        if len(shortcode) > config['max_short_url_length']:
            self.mainUi.shorturl_edit.setPlaceholderText(f"Shortcode must be at most {config['max_short_url_length']} characters long")
            return
        
        database.insert_url(url, shortcode)
        self.addUrlToTable(url, shortcode)
        self.mainUi.shorturl_edit.setPlaceholderText("Shortcode")
        self.mainUi.longurl_edit.setText("")
        
        
    def clearfields(self):
        self.mainUi.clearBtn.setText("Clear")
        self.mainUi.longurl_edit.setText("")
        self.mainUi.shorturl_edit.setText("")
        self.mainUi.shorturl_edit.setPlaceholderText("Shortcode")
        self.mainUi.AddButton.setText("Add URL")
        self.mainUi.deleteBtn.hide()
        
    # Check if the user wants to use custom shortcode
    def isCustomShortCode(self) -> bool:
        return self.mainUi.custom_shortcode.checkState() == 2 and True or False
    
        
    def customShortcode(self):
        self.mainUi.shorturl_edit.setReadOnly(not self.isCustomShortCode())
        
    
    def cellClicked(self):
        row = self.mainUi.DataTable.currentRow()
        shortcode = self.mainUi.DataTable.item(row, 1).text()
        url = self.mainUi.DataTable.item(row, 0).text()
        
        if self.mainUi.DataTable.currentColumn() == 3:
            database.delete_url(shortcode)
            self.mainUi.DataTable.removeRow(row)
        else:
            self.mainUi.longurl_edit.setText(url)
            self.mainUi.shorturl_edit.setText(shortcode)
            self.mainUi.shorturl_edit.setReadOnly(True)
            self.mainUi.custom_shortcode.setCheckState(0)
            self.mainUi.deleteBtn.show()
            self.mainUi.shorturl_edit.setPlaceholderText("Shortcode")
            self.mainUi.clearBtn.setText("Add URL")
            self.mainUi.AddButton.setText("Update URL")
            
    
    def deleteSelectedUrl(self):
        self.clearfields()
        row = self.mainUi.DataTable.currentRow()
        shortcode = self.mainUi.DataTable.item(row, 1).text()
        database.delete_url(shortcode)
        self.mainUi.DataTable.removeRow(row)
        
        
    # Open settings dialog
    def settings(self):
        if self.settingsUi.exec():
            print("Settings saved")
        else:
            print("Settings not saved")


    def closeEvent(self, event):
        router.shutdown_server()  # Shutdown the router server
        event.accept()

if __name__ == "__main__":
    window()