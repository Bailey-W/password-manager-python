import logger
logger.log_event("Started process", __name__)
import db_manager
import keygen
# Adds a new entry to the database
# Expects: username, as string used to login to the site
#          password, the plaintext version of the password
#          url, the url of the site

master_key = b''

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

def login(password: str) -> bool:
    logger.log_event('Attempting login...', __name__)
    correct = keygen.verify_password(password)
    if not correct:
        logger.log_event('Login failed', __name__)
        return False
    logger.log_event('Login successful')
    master_key = keygen.generate_key_from_password(password)
    return True