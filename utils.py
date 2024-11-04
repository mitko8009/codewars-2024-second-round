class URLShortcode:
    def __init__(self, url, shortcode):
        self.url = url
        self.shortcode = shortcode
        
    def url(self):
        return self.url
    
    def shortcode(self):
        return self.shortcode
    

if __name__ == "__main__":
    from main import window
    window()