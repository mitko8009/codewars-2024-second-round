import json
import sys
import os

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
    with open("./config.json", "r") as f:
        return json.load(f)[key]
    
# Toggle all elements in a layout
def toggleAllElementFromLayout(layout, state):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget:
            widget.setVisible(state)

if __name__ == "__main__":
    from main import window
    window()