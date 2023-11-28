# Creates a new SQLite Database with the expected schema
def create_database():
    pass

# Checks if a SQLite Database already exists
def check_for_db() -> bool:
    pass

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