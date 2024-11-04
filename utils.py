import sys
import os

class URLShortcode:
    def __init__(self, url, shortcode):
        self.url = url
        self.shortcode = shortcode
        
    def url(self) -> str:
        return self.url
    
    def shortcode(self) -> str:
        return self.shortcode
    
# Get the path of a resource file
def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)
    

if __name__ == "__main__":
    from main import window
    window()