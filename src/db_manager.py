import sqlite3
import os
import logger

def setup_db(connection):
    logger.log_event("Setting up database for first run")
    cur = connection.cursor()
    cur.execute("CREATE TABLE entries(username, url, password)")
    logger.log_event("Database setup complete")

# Connects to the SQLite database. Creates the database if it does not exist.
# Returns: a database connection object
def connect_to_db():
    db_location = os.path.dirname(os.path.abspath(__file__)) + "/../data/data.db"
    
    is_new_db = not os.path.isfile(db_location)

    logger.log_event("Connecting to database")
    con = sqlite3.connect(db_location)
    logger.log_event("Successfully connected to database")

    if is_new_db:
        setup_db(con)

    return con

# Finds the password(s) matching the query
# Expects: username, the username to find
#          url, the url to find
# Returns: A list of encrypted passwords which match both the username and url
def get_encrypted_passwords(username: str, url: str) -> list:
    pass

# Finds entries which contain the query string
# Expects: query, the string to search for
# Returns: A list of all entries containing the query in either username or url fields
def find_entries_containing(query: str) -> list:
    pass

connect_to_db()