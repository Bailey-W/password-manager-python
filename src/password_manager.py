import logger
logger.log_event("Started process", __name__)
import db_manager
import keygen
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import os
import secrets

master_key = b''

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


def gen_or_get_initial_vector():
    logger.log_event('Looking for IV...', __name__)
    iv_location = os.path.dirname(os.path.abspath(__file__)) + "/../keys/iv.key"
    iv = b''
    if os.path.isfile(iv_location):
        logger.log_event('IV found!', __name__)
        # read salt from file
        f = open(iv_location, 'rb')
        iv = f.readline()
        f.close()
    else:
        logger.log_event('IV not found. Generating IV', __name__)
        iv = os.urandom(16)
        f = open(iv_location, 'wb')
        f.write(iv)
        f.close()
    
    return iv
    

# Generates a strong password
# Returns: the auto-generated password
def generate_password() -> str:
    logger.log_event('Generating random password', __name__)
    password_length = 16
    return secrets.token_urlsafe(password_length)

# Encrpyts a plaintext string using the generated AES Key
def encrypt(plaintext: str):
    plaintext = bytes(plaintext, encoding='utf-8')
    logger.log_event('Encrypting...', __name__)
    if not master_key:
        logger.log_event('Error: Not logged in', __name__)
        return None
    
    logger.log_event('Padding password', __name__)
    padder = PKCS7(256).padder()
    padded = padder.update(plaintext)
    padded += padder.finalize()

    logger.log_event('Encrypting Passowrd', __name__)
    cipher = Cipher(algorithms.AES(master_key), modes.CBC(gen_or_get_initial_vector()))
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()

# Decrypts ciphertext that was encrypted with the AES Key
def decrypt(ciphertext) -> str:
    logger.log_event('Encrypting...', __name__)
    if not master_key:
        logger.log_event('Error: Not logged in', __name__)
        return None
    
    logger.log_event('Decrypting password', __name__)
    cipher = Cipher(algorithms.AES(master_key), modes.CBC(gen_or_get_initial_vector()))
    decryptor = cipher.decryptor()
    text = decryptor.update(ciphertext) + decryptor.finalize()

    logger.log_event('Unpadding password', __name__)
    unpadder = PKCS7(256).unpadder()
    unpadded = unpadder.update(text)
    unpadded += unpadder.finalize()

    return unpadded.decode('utf-8')

def login(password: str) -> bool:
    global master_key
    logger.log_event('Attempting login...', __name__)
    correct = keygen.verify_password(password)
    if not correct:
        logger.log_event('Login failed', __name__)
        return False
    logger.log_event('Login successful')
    master_key = keygen.generate_key_from_password(password)
    return True