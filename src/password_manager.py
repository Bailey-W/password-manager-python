
# Adds a new entry to the database
# Expects: username, as string used to login to the site
#          password, the plaintext version of the password
#          url, the url of the site
# Returns: True if the entry was successfully added, False if there was an error
def add_entry(username: str, password: str, url: str) -> bool:
    pass

# Adds a new entry to the database with auto-generated password
# Expects: username, as string used to login to the site
#          url, the url of the site
# Returns: True if the entry was successfully added, False if there was an error
def add_entry_with_generated_password(username: str, url: str) -> bool:
    password = generate_password()
    return add_entry(username, password, url)

# Generates a strong password
# Returns: the auto-generated password
def generate_password() -> str:
    pass

# Encrpyts a plaintext string using the generated AES Key
def encrypt(plaintext: str) -> str:
    pass

# Decrypts ciphertext that was encrypted with the AES Key
def decrypt(ciphertext: str) -> str:
    pass