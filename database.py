import sqlite3
import uuid

import utils

# Connect to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create database table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        shortcode TEXT PRIMARY KEY,
        url TEXT NOT NULL
    )
''')
conn.commit()

######################
# Database functions #
######################

def shortcode_exists(shortcode: str) -> bool:
    cursor.execute('SELECT 1 FROM urls WHERE shortcode = ?', (shortcode,))
    return cursor.fetchone() is not None


def insert_url(url: str, shortcode: str = None):
    if shortcode is None:
        shortcode = generate_unique_shortcode()
    
    cursor.execute('INSERT INTO urls (shortcode, url) VALUES (?, ?)', (shortcode, url))
    conn.commit()
    
# Generate a unique shortcode using hex representation of a UUID
def generate_unique_shortcode() -> str:
    while True:
        shortcode = uuid.uuid4().hex[:6]
        if not shortcode_exists(shortcode):
            return shortcode
    
# Get URL from shortcode
def get_url(shortcode) -> str:
    cursor.execute('SELECT url FROM urls WHERE shortcode = ?', (shortcode,))
    result = cursor.fetchone()
    return result[0] if result else None

# Get all URLs in a list of URLShortcode objects
def get_all_urls() -> list[utils.URLShortcode]:
    cursor.execute('SELECT * FROM urls')
    return [utils.URLShortcode(url, shortcode) for shortcode, url in cursor.fetchall()]


def update_url(shortcode, new_url):
    cursor.execute('UPDATE urls SET url = ? WHERE shortcode = ?', (new_url, shortcode))
    conn.commit()
    
    
def delete_url(shortcode):
    cursor.execute('DELETE FROM urls WHERE shortcode = ?', (shortcode,))
    conn.commit()
    
        
def delete_all():
    cursor.execute('DELETE FROM urls')
    conn.commit()


# Test the database functions    
if __name__ == '__main__':
    input('This will delete all data in the database.\nPress Enter to continue...')
    delete_all()
    for i in range(10):
        print(i)
        insert_url(f'https://example.com/{i}')
    print(get_all_urls()[0].url)
    print(get_all_urls()[0].shortcode)
    from main import window
    window()
