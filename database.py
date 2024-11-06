import sqlite3
import uuid

import utils

# Connect to database
db_config = utils.getFromConfig("database")
db_name = db_config.get('db_name', 'database')
hostname = db_config.get('hostname', 'localhost')
port = db_config.get('port', 27017)

if db_config.get('remote'):
    conn = sqlite3.connect(f"file:{hostname}:{port}/{db_name}?mode=rw", uri=True, check_same_thread=False)
else:
    conn = sqlite3.connect(f"{db_name}.db", check_same_thread=False)
    
cursor = conn.cursor()

# Create database table
database_base = '''
    CREATE TABLE IF NOT EXISTS urls (
        shortcode TEXT PRIMARY KEY,
        url TEXT NOT NULL,
        metadata TEXT
    )
'''
cursor.execute(database_base)
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
        shortcode = uuid.uuid4().hex[:utils.getFromConfig("short_url_length")]
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
    return [utils.URLShortcode(url, shortcode, metadata) for shortcode, url, metadata in cursor.fetchall()]


def update_url(shortcode, new_url) -> None:
    cursor.execute('UPDATE urls SET url = ? WHERE shortcode = ?', (new_url, shortcode))
    conn.commit()
    
    
def delete_url(shortcode) -> None:
    cursor.execute('DELETE FROM urls WHERE shortcode = ?', (shortcode,))
    conn.commit()
    

def purgeAllData() -> None:
    cursor.execute('DROP TABLE urls')
    conn.commit()
    cursor.execute(database_base)
    conn.commit()
    

def appendMetadata(shortcode: str, key: str, value: str) -> None:
    cursor.execute('SELECT metadata FROM urls WHERE shortcode = ?', (shortcode,))
    metadata = cursor.fetchone()[0]
    if metadata is None or metadata == 'None':
        metadata = {}
    else:
        metadata = eval(metadata)
    metadata[key] = value
    cursor.execute('UPDATE urls SET metadata = ? WHERE shortcode = ?', (str(metadata), shortcode))
    conn.commit()


# Test the database functions    
if __name__ == '__main__':
    input('This will purge all data in the database.\nPress Enter to continue...')
    purgeAllData()
    for i in range(10):
        print(i)
        insert_url(f'https://example.com/{i}', f'{i}{i}{i}')
    
    appendMetadata('000', 'locked', 'true')
    appendMetadata('000', 'password', 'hunter2')
    print(get_all_urls()[0].url)
    print(get_all_urls()[0].shortcode)
    print(eval(get_all_urls()[0].metadata)['locked'])
    # print(eval(get_all_urls()[0].metadata))
    from main import window
    window()
