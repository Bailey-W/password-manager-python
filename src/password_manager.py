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
    encrypted_password = encrypt(password)                                              # Encrpyts the password
    logger.log_event('Adding new entry', __name__)
    db_manager.insert_new_entry(username, encrypted_password, url)                      # Adds the username, encrypted password, and url to the database

# Adds a new entry to the database with auto-generated password
# Expects: username, as string used to login to the site
#          url, the url of the site
def add_entry_with_generated_password(username: str, url: str):
    logger.log_event('Adding new entry with random password', __name__)
    password = generate_password()                                                      # Generates a password
    add_entry(username, password, url)                                                  # Stores the username, url, and newly generated password in the database

# Looks up a password by username and url
# Expects: username, a string that corresponds to the desired username
#          url, the url of the corresponding site
# Returns: the decrypted password
def get_password_for_entry(username: str, url: str) -> str:
    logger.log_event(f'Looking for password, user: {username}, site: {url}', __name__)  # Logs the lookup
    data = db_manager.get_encrypted_passwords(username, url)                            # Looks up the encrypted password in the database
    if not data:                                                                        # Handles if the password cannot be found
        logger.log_event('Password not found...', __name__)
        return None
    logger.log_event('Password found', __name__)
    password = data[0][2]                                                               # Finds the first password in the returned list
    password = decrypt(password)                                                        # Decrypts the password

    return password                                                                     # Returns the decrypted password

# Gets the initial vector if it exists, or generates and saves one
#
# Note: the initial vector is used for the AES encryption and decryption
def gen_or_get_initial_vector():
    logger.log_event('Looking for IV...', __name__)
    iv_location = os.path.dirname(os.path.abspath(__file__)) + "/../keys/iv.key"        # Looks for the IV file
    iv = b''
    if os.path.isfile(iv_location):                                                     # If the IV file is found,
        logger.log_event('IV found!', __name__)
        # read salt from file
        f = open(iv_location, 'rb')                                                     # Read the IV
        iv = f.readline()
        f.close()
    else:
        logger.log_event('IV not found. Generating IV', __name__)                       # IV not found
        iv = os.urandom(16)                                                             # Generates a random IV
        f = open(iv_location, 'wb')                                                     # Saves IV to file for later use
        f.write(iv)
        f.close()
    
    return iv                                                                           # Return IV
    

# Generates a strong password
# Returns: the auto-generated password
def generate_password() -> str:
    logger.log_event('Generating random password', __name__)
    password_length = 16
    return secrets.token_urlsafe(password_length)                                       # The secrets library allows the easy generation of a secure password

# Encrpyts a plaintext string using the generated AES Key
def encrypt(plaintext: str):
    plaintext = bytes(plaintext, encoding='utf-8')                                      # The plaintext needs to be in bytes
    logger.log_event('Encrypting...', __name__)
    if not master_key:
        logger.log_event('Error: Not logged in', __name__)                              # Checks to make sure the user has logged in (there won't be a master key if they haven't)
        return None
    
    logger.log_event('Padding password', __name__)
    padder = PKCS7(256).padder()                                                        # Pads the plaintext to fit in a block size
    padded = padder.update(plaintext)
    padded += padder.finalize()

    logger.log_event('Encrypting Passowrd', __name__)
    cipher = Cipher(algorithms.AES(master_key), modes.CBC(gen_or_get_initial_vector())) # Creates an AES cipher using the master key and the IV (see gen_or_get_initial_vector function)
    encryptor = cipher.encryptor()                                                      # Creates an encryptor object using the cypher
    return encryptor.update(padded) + encryptor.finalize()                              # Uses the encryptor object to encrypt the string, returns that value

# Decrypts ciphertext that was encrypted with the AES Key
def decrypt(ciphertext) -> str:
    logger.log_event('Encrypting...', __name__)
    if not master_key:                                                                  # Checks to see if the user is logged in
        logger.log_event('Error: Not logged in', __name__)
        return None
    
    logger.log_event('Decrypting password', __name__)                                   # Starts by decrypting the ciphertext
    cipher = Cipher(algorithms.AES(master_key), modes.CBC(gen_or_get_initial_vector())) # Generates the same sipher as the encrypt function, using the master key and same IV
    decryptor = cipher.decryptor()
    text = decryptor.update(ciphertext) + decryptor.finalize()                          # Stores the decrypted text in a variable

    logger.log_event('Unpadding password', __name__)
    unpadder = PKCS7(256).unpadder()                                                    # The padding from encrypt() needs to be undone (unpadded)
    unpadded = unpadder.update(text)
    unpadded += unpadder.finalize()                                                     # Stores the unpadded result

    return unpadded.decode('utf-8')                                                     # Converts the unpadded result back to a string (from bytes) and returns that value

# Takes a password and checks if its correct, then retrieves the master key
# Expects: password, a string containing the password
# Returns: True if the user is now logged in, False if the password was incorrect
def login(password: str) -> bool:
    global master_key
    logger.log_event('Attempting login...', __name__)
    correct = keygen.verify_password(password)                                          # Uses the verify_password function to check if the password matches (using hashes)
    if not correct:                                                                     # Stops here and returns false if the password does not match
        logger.log_event('Login failed', __name__)
        return False
    logger.log_event('Login successful')                                                # The password matches!
    master_key = keygen.generate_key_from_password(password)                            # Generates the master key from the password and stores it for later use
    return True