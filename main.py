from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
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
        
        self.functionality()
        
        self.mainUi.show()
        sys.exit(app.exec_())
       
    # Load the theme
    def loadTheme(self, file, app):
        theme = QFile(utils.resource_path(file))
        if theme.open(QFile.ReadOnly | QFile.Text):
            qss = theme.readAll()
            app.setStyleSheet(str(qss, encoding='utf-8'))
            theme.close()

    # Functionality of the application
    def functionality(self):
        self.refreshTable()
        self.mainUi.shorturl_edit.setReadOnly(True)
        self.mainUi.custom_shortcode.clicked.connect(self.customShortcode)
        
        # Set time and date
        self.mainUi.expireDate.setDate(QDate.currentDate())
        self.mainUi.expireDate.setDateTime(QDateTime.currentDateTime().addSecs(1800))
        self.mainUi.expireDate.setMinimumDate(QDate.currentDate())
        
        
        # Button actions
        self.mainUi.AddButton.clicked.connect(self.addUrl)
        self.mainUi.clearBtn.clicked.connect(self.clearfields)
        self.mainUi.deleteBtn.hide()
        self.mainUi.deleteBtn.clicked.connect(self.deleteSelectedUrl)
        self.mainUi.copyLongURL.clicked.connect(lambda: pyperclip.copy(self.mainUi.longurl_edit.text()))
        self.mainUi.copyLongURL.hide()
        self.mainUi.copyShortURL.clicked.connect(lambda: pyperclip.copy(len(self.mainUi.shorturl_edit.text()) > 0 and  f"localhost:{config['flask_port']}/{self.mainUi.shorturl_edit.text()}" or ""))
        self.mainUi.copyShortURL.hide()
        self.mainUi.AdvancedSettingsBox.hide()
        self.mainUi.AdvancedSettings.clicked.connect(lambda: utils.toggleVisibility(self.mainUi.AdvancedSettingsBox))
        self.mainUi.expireDate.hide()
        self.mainUi.expireDateBtn.clicked.connect(lambda: utils.toggleVisibility(self.mainUi.expireDate))
        self.mainUi.passwordBox.hide()
        self.mainUi.passwordBtn.clicked.connect(lambda: utils.toggleVisibility(self.mainUi.passwordBox))
        self.mainUi.maxUses.hide()
        self.mainUi.limitURLUsesBtn.clicked.connect(lambda: utils.toggleVisibility(self.mainUi.maxUses))
        self.mainUi.refreshBtn.clicked.connect(self.refreshTable)
        self.mainUi.CheckURLBtn.clicked.connect(self.checkURL)
        
        # Table actions
        self.mainUi.DataTable.cellClicked.connect(self.cellClicked)
        
        # Menu actions
        self.mainUi.actionSettings.triggered.connect(self.settings)
        self.mainUi.actionNew_URL.triggered.connect(self.clearfields)
        self.mainUi.actionQuit.triggered.connect(self.close)
        self.mainUi.actionRefresh_Table.triggered.connect(self.refreshTable)
        self.mainUi.actionClear_Fields.triggered.connect(self.clearfields)
        
        
        #### Settings dialog
        self.settingsUi.label_settings.setText(f"{config['title']} Settings")
        self.settingsUi.RemoteGroup.hide()
        self.settingsUi.remoteDb.clicked.connect(lambda: utils.toggleVisibility(self.settingsUi.RemoteGroup)) 
        self.settingsUi.purgeBtn.clicked.connect(self.purgeDatabase)
        
    
    def addUrlToTable(self, url, shortcode):
        table = self.mainUi.DataTable
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, QTableWidgetItem(shortcode))
        table.setItem(rowPosition, 1, QTableWidgetItem(url))
        
    # Add a new URL to the database
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
        
        # Check if the password is valid
        if self.mainUi.passwordBox.text() != "" and self.passwordBtn.isChecked():
            password = utils.hashPassword(self.mainUi.passwordBox.text())
            if "'" in password or '"' in password:
                self.mainUi.passwordBox.setPlaceholderText("Invalid password")
                return
        else:
            password = None

        # Add exparation date if the user wants to        
        if self.mainUi.expireDateBtn.isChecked():
            expireDate = self.mainUi.expireDate.dateTime().toSecsSinceEpoch()
        else:
            expireDate = None
            
        # Add max uses if the user wants to
        if self.mainUi.maxUses.value() > 0 and self.mainUi.limitURLUsesBtn.isChecked():
            uses = self.mainUi.maxUses.value()
        else:
            uses = None
            
                        
        # Database
        database.insert_url(url, shortcode)
        database.appendMetadata(shortcode, "password", password)
        database.appendMetadata(shortcode, "expires", expireDate)
        database.appendMetadata(shortcode, "maxUses", uses)
        database.appendMetadata(shortcode, "uses", 0)
        
        self.addUrlToTable(url, shortcode)
        self.clearfields()
        
    
    def updateUrl(self):
        url = self.mainUi.longurl_edit.text()
        shortcode = self.mainUi.shorturl_edit.text()
        database.update_url(shortcode, url)
        self.deleteSelectedUrl()
        self.clearfields()
        self.addUrlToTable(url, shortcode)
        
    # Clear the fields and set the button state to "Add URL"
    def clearfields(self):
        self.mainUi.AddButton.disconnect()
        self.mainUi.AddButton.clicked.connect(self.addUrl)
        
        self.mainUi.AdvancedSettings.setChecked(False)
        self.mainUi.AdvancedSettings.show()
        
        self.mainUi.clearBtn.setText("Clear")
        self.mainUi.AddButton.setText("Add URL")
        self.mainUi.longurl_edit.setText("")
        self.mainUi.shorturl_edit.setText("")
        self.mainUi.passwordBox.setText("")
        self.mainUi.urlcheckEdit.setText("")
        self.mainUi.shorturl_edit.setPlaceholderText("Shortcode")
        self.mainUi.passwordBox.setPlaceholderText("Password")
        self.mainUi.deleteBtn.hide()
        self.mainUi.copyShortURL.hide()
        self.mainUi.copyLongURL.hide()
        self.mainUi.passwordBox.setReadOnly(False)
        
    # Check if the user wants to use custom shortcode
    def isCustomShortCode(self) -> bool:
        return self.mainUi.custom_shortcode.checkState() == 2 and True or False
    
    # Enable or disable the custom shortcode field
    def customShortcode(self):
        self.mainUi.shorturl_edit.setReadOnly(not self.isCustomShortCode())
        
    # When a cell is clicked in the table
    def cellClicked(self):
        row = self.mainUi.DataTable.currentRow()
        shortcode = self.mainUi.DataTable.item(row, 0).text()
        url = self.mainUi.DataTable.item(row, 1).text()
        
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
            self.mainUi.passwordBox.setReadOnly(True)
            self.mainUi.passwordBox.setPlaceholderText("You can't change the password")
            self.mainUi.passwordBox.setText("")
            self.mainUi.copyShortURL.show()
            self.mainUi.copyLongURL.show()
            self.mainUi.AdvancedSettings.hide()
            
    
    def deleteSelectedUrl(self):                                                                                                
        row = self.mainUi.DataTable.currentRow()
        shortcode = self.mainUi.DataTable.item(row, 0).text()
        database.delete_url(shortcode)
        self.clearfields()
        self.mainUi.DataTable.removeRow(row)
        
    
    def refreshTable(self):
        self.mainUi.DataTable.setRowCount(0)
        self.clearfields()
        
        # Load data from database
        data = database.get_all_urls()
        for i in data:
            url = i.url
            metadata = eval(i.metadata)
            
            if metadata['password'] is not None and config['rename_password_protected_urls']:
                url = "Password protected URL"
                
            if "hidden" in metadata.keys() and metadata['hidden'] == True and not config['show_hidden_urls']:
                continue
            
            self.addUrlToTable(url, i.shortcode)
            
    
    def checkURL(self):
        search_text = self.mainUi.urlcheckEdit.text()
        
        if "/" in search_text:
            search_text = search_text.split("/")[-1]
        
        table = self.mainUi.DataTable
        for row in range(table.rowCount()):
            item = table.item(row, 0)  # Assuming the short URL is in the first column
            if item and item.text() == search_text:
                table.selectRow(row)
                self.cellClicked()
                return
            
        QMessageBox.information(self, "Search Result", "Short URL not found.")
        
    # Open settings dialog
    def settings(self):
        # Set values from config
        ## General
        self.settingsUi.max_short_url_length.setValue(config['max_short_url_length'])
        self.settingsUi.short_url_length.setValue(config['short_url_length'])
        self.settingsUi.renamepasswdurls.setChecked(config['rename_password_protected_urls'])
        self.settingsUi.showHiddenUrls.setChecked(config['show_hidden_urls'])
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
            config['rename_password_protected_urls'] = self.settingsUi.renamepasswdurls.isChecked()
            config['show_hidden_urls'] = self.settingsUi.showHiddenUrls.isChecked()
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
                
            # Update table
            self.refreshTable()
                
    
    def purgeDatabase(self):
        database.purgeAllData()
        self.refreshTable()

    # Close the application and shutdown the router server
    def closeEvent(self, event):
        router.shutdown_server()  # Shutdown the router server
        event.accept()

def main():
    utils.clearConsole()
    try:
        window()
    except Exception as e:
        print("\n\n\nERROR CODE:\n"+str(e)+"\n\n\n")
        router.shutdown_server()

if __name__ == "__main__":
    main()
    
