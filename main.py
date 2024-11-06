from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
import threading
import pyperclip
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
        self.mainUi.setWindowTitle(config["title"]+"  v"+config["version"])
        self.mainUi.setWindowIcon(QIcon(utils.resource_path("assets/icon.png")))
        
        self.settingsUi = uic.loadUi(utils.resource_path("ui/settings.ui"))
        self.settingsUi.setWindowTitle("Settings")
        self.settingsUi.setWindowIcon(QIcon(utils.resource_path("assets/icon.png")))
        self.settingsUi.setParent(self.mainUi)
        self.settingsUi.setWindowFlags(Qt.WindowFlags(Qt.Dialog))
        
        # Load theme
        if not config['default_theme']:
            self.loadTheme("ui/theme.qss", app)
            self.loadTheme("ui/theme.qss", self.settingsUi)
        
        self.functionality()
        
        self.mainUi.show()
        sys.exit(app.exec_())
       
        
    def loadTheme(self, file, app):
        theme = QFile(utils.resource_path(file))
        if theme.open(QFile.ReadOnly | QFile.Text):
            qss = theme.readAll()
            app.setStyleSheet(str(qss, encoding='utf-8'))
            theme.close()

     
    def functionality(self):
        # Load data from database
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
        utils.toggleAllElementFromLayout(self.mainUi.passwordLayout, False)
        self.mainUi.passwordBtn.clicked.connect(self.password)
        utils.toggleAllElementFromLayout(self.mainUi.usesLimitLayout, False)
        self.mainUi.usesLimitBtn.clicked.connect(self.usesLimit)
        self.mainUi.copyLongURL.clicked.connect(lambda: pyperclip.copy(self.mainUi.longurl_edit.text()))
        self.mainUi.copyShortURL.clicked.connect(lambda: pyperclip.copy(len(self.mainUi.shorturl_edit.text()) > 0 and  f"localhost:{config['flask_port']}/{self.mainUi.shorturl_edit.text()}" or ""))
        
        # Table actions
        self.mainUi.DataTable.cellClicked.connect(self.cellClicked)
        
        # Menu actions
        self.mainUi.actionSettings.triggered.connect(self.settings)
        self.mainUi.actionNew_URL.triggered.connect(self.clearfields)
        self.mainUi.actionQuit.triggered.connect(self.close)
        
        
        
        #### Settings dialog
        self.settingsUi.label_settings.setText(f"{config['title']} Settings")
        self.settingsUi.RemoteGroup.hide()
        self.settingsUi.remoteDb.clicked.connect(self.remoteDb)
        self.settingsUi.purgeBtn.clicked.connect(database.purgeAllData)
        
    
    def addUrlToTable(self, url, shortcode):
        table = self.mainUi.DataTable
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, QTableWidgetItem(shortcode))
        table.setItem(rowPosition, 1, QTableWidgetItem(url))
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
        
    
    def updateUrl(self):
        url = self.mainUi.longurl_edit.text()
        shortcode = self.mainUi.shorturl_edit.text()
        self.deleteSelectedUrl()
        database.update_url(shortcode, url)
        self.clearfields()
        self.addUrlToTable(url, shortcode)
        
    # Clear the fields and set the button state to "Add URL"
    def clearfields(self):
        self.mainUi.clearBtn.setText("Clear")
        self.mainUi.longurl_edit.setText("")
        self.mainUi.shorturl_edit.setText("")
        self.mainUi.shorturl_edit.setPlaceholderText("Shortcode")
        self.mainUi.AddButton.setText("Add URL")
        self.mainUi.AddButton.disconnect()
        self.mainUi.AddButton.clicked.connect(self.addUrl)
        self.mainUi.deleteBtn.hide()
        
    # Check if the user wants to use custom shortcode
    def isCustomShortCode(self) -> bool:
        return self.mainUi.custom_shortcode.checkState() == 2 and True or False
    
    # Enable or disable the custom shortcode field
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
            self.mainUi.AddButton.disconnect()
            self.mainUi.AddButton.clicked.connect(self.updateUrl)
            
    
    def deleteSelectedUrl(self):
        self.clearfields()
        row = self.mainUi.DataTable.currentRow()
        shortcode = self.mainUi.DataTable.item(row, 1).text()
        database.delete_url(shortcode)
        self.mainUi.DataTable.removeRow(row)
        
    
    def usesLimit(self):
        if self.mainUi.usesLimitBtn.isChecked():
            utils.toggleAllElementFromLayout(self.mainUi.usesLimitLayout, True)
        else:
            utils.toggleAllElementFromLayout(self.mainUi.usesLimitLayout, False)
        
        
    def password(self):
        if self.mainUi.passwordBtn.isChecked():
            utils.toggleAllElementFromLayout(self.mainUi.passwordLayout, True)
        else:
            utils.toggleAllElementFromLayout(self.mainUi.passwordLayout, False)
        
        
    # Open settings dialog
    def settings(self):
        # Set values from config
        ## General
        self.settingsUi.max_short_url_length.setValue(config['max_short_url_length'])
        self.settingsUi.short_url_length.setValue(config['short_url_length'])
        ## Appearance
        self.settingsUi.defaultTheme.setChecked(config['default_theme'])
        ## Database
        self.settingsUi.DatabaseName.setText(config['database']['db_name'])
        self.settingsUi.remoteDb.setChecked(config['database']['remote'])
        self.settingsUi.hostName.setText(config['database']['hostname'])
        self.settingsUi.hostPort.setText(str(config['database']['port']))
        ## Flask
        self.settingsUi.routerDebug.setChecked(config['flask_debug'])
        self.settingsUi.routerPort.setText(str(config['flask_port']))
        
        
        if self.settingsUi.exec():
            print("Settings saved")
            # Save values to config
            config['max_short_url_length'] = self.settingsUi.max_short_url_length.value()
            config['short_url_length'] = self.settingsUi.short_url_length.value()
            config['default_theme'] = self.settingsUi.defaultTheme.isChecked()
            config['database']['db_name'] = self.settingsUi.DatabaseName.text()
            config['database']['remote'] = self.settingsUi.remoteDb.isChecked()
            config['database']['hostname'] = self.settingsUi.hostName.text()
            config['database']['port'] = int(self.settingsUi.hostPort.text())
            config['flask_debug'] = self.settingsUi.routerDebug.isChecked()
            config['flask_port'] = int(self.settingsUi.routerPort.text())
            utils.saveConfig(config)
            
            # Update the theme
            if config['default_theme']:
                QApplication.instance().setStyleSheet("")
            else:
                self.loadTheme("ui/theme.qss", QApplication.instance())
                
            print(self.settingsUi.exec())
            
    
    def remoteDb(self):
        if self.settingsUi.remoteDb.isChecked():
            self.settingsUi.RemoteGroup.show()
        else:
            self.settingsUi.RemoteGroup.hide()


    def closeEvent(self, event):
        router.shutdown_server()  # Shutdown the router server
        event.accept()

if __name__ == "__main__":
    window()
    
