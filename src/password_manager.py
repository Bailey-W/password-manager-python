import logger
logger.log_event("Started process", __name__)
import db_manager
# Adds a new entry to the database
# Expects: username, as string used to login to the site
#          password, the plaintext version of the password
#          url, the url of the site
def add_entry(username: str, password: str, url: str):
    encrypted_password = encrypt(password)
    logger.log_event('Adding new entry', __name__)
    db_manager.insert_new_entry(username, encrypted_password, url)

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
    logger.log_event('Encrypting...', __name__)
    return plaintext

# Decrypts ciphertext that was encrypted with the AES Key
def decrypt(ciphertext: str) -> str:
    logger.log_event('Decrypting...', __name__)
    return ciphertext