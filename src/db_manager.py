import logger
logger.log_event('Started process', __name__)
import sqlite3
import os

con = None

def setup_db():
    global con
    logger.log_event("Setting up database for first run", __name__)
    cur = con.cursor()
    cur.execute("CREATE TABLE entries(username, url, password)")
    logger.log_event("Database setup complete", __name__)

# Connects to the SQLite database. Creates the database if it does not exist.
# Returns: a database connection object
def connect_to_db():
    global con
    db_location = os.path.dirname(os.path.abspath(__file__)) + "/../data/wimerDB.db"
    
    is_new_db = not os.path.isfile(db_location)

    logger.log_event("Connecting to database", __name__)
    con = sqlite3.connect(db_location)
    logger.log_event("Successfully connected to database", __name__)

    if is_new_db:
        setup_db()

    return con

# Finds the password(s) matching the query
# Expects: username, the username to find
#          url, the url to find
# Returns: A list of encrypted passwords which match both the username and url
def get_encrypted_passwords(username: str, url: str) -> list:
    global con
    cur = con.cursor()
    cur.execute('SELECT * FROM entries WHERE username=? AND url=?', (username, url))
    return cur.fetchall()

def insert_new_entry(username, encrpyted_password, url):
    global con
    cur = con.cursor()
    params = (username, url, encrpyted_password)
    cur.execute('INSERT INTO entries (username, url, password) VALUES (?, ?, ?)', params)
    con.commit()
    logger.log_event(f'Inserted "{username}" into database', __name__)

connect_to_db()