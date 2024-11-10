from PyQt5.QtWidgets import QWidget
import hashlib
import json
import time
import sys
import os

from init import initConfig

# URLShortcode class to store URL, shortcode and metadata
class URLShortcode:
    def __init__(self, url, shortcode, metadata):
        self.url = url
        self.shortcode = shortcode
        self.metadata = metadata
        
    def url(self) -> str:
        return self.url
    
    def shortcode(self) -> str:
        return self.shortcode
    
    def metadata(self) -> str:
        return self.metadata
    
# Get the path of a resource file
def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

# Save the configuration file
def saveConfig(config: dict) -> None:
    with open("./config.json", "w") as f:
        json.dump(config, f, indent="\t")
        
# Get a value from the configuration file
def getFromConfig(key: str) -> str:
    if not os.path.exists("./config.json"):
        initConfig()
    
    with open("./config.json", "r") as f:
        return json.load(f)[key]
    
# Toggle the visibility of a widget
def toggleVisibility(widget: QWidget) -> None:
    widget.setVisible(not widget.isVisible())
            
# Get the current timestamp
def getTimestamp() -> int:
    return int(time.time())

# Clear the console
def clearConsole() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    
# Get a file's contents
def getFileContents(file: str) -> str:
    with open(file, "r") as f:
        return f.read()

# Hash a password
def hashPassword(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Route for URL not found
def URLNotFoundRoute() -> str:
    return getFileContents(resource_path("./static/error.html")).format(
        app_title=getFromConfig("title"),
        css=getFileContents(resource_path("./static/style.css")),
        title="URL not found<br>404",
        content="This URL does not exist."
    )

if __name__ == "__main__":
    from main import main
    main()