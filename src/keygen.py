import logger
logger.log_event("Starting process", __name__)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

# Reads salt from file if it exists,
# otherwise, generates new salt and saves to file
def gen_or_get_salt():
    logger.log_event('Looking for salt...', __name__)
    salt_location = os.path.dirname(os.path.abspath(__file__)) + "/../keys/salt.key"                # The location of the salt file
    salt = b''
    if os.path.isfile(salt_location):                                                               # Checks if the salt file exists
        logger.log_event('Salt found!', __name__)
        # read salt from file
        f = open(salt_location, 'rb')                                                               # Since the salt file exists, reads it, then eventually returns the read salt
        salt = f.readline()
        f.close()
    else:
        logger.log_event('Salt not found. Generating Salt', __name__)                               # The salt file doesn't exist
        salt = os.urandom(16)                                                                       # Generates a new random salt
        f = open(salt_location, 'wb')                                                               # Creates the salt file
        f.write(salt)                                                                               # Stores the salt in the file
        f.close()
    
    return salt                                                                                     # Return either the read salt or newly generated

# Generates a SHA256 key from a given password
# Expects: password, a string containing the password
# Returns: key, a byte string containing the master key
def generate_key_from_password(password):
    logger.log_event("Generating master key from master password", __name__)
    password = bytes(password, encoding='utf-8')                                                    # Converts the password to bytes
    kdf = PBKDF2HMAC(                                                                               # Sets up the PBKDF2 Algorithm for generating the key
        algorithm=hashes.SHA256(),
        length=32,
        salt=gen_or_get_salt(),
        iterations=480000,
    )
    key = kdf.derive(password)                                                                      # Derives the master key
    return key
    

# Checks if the entered password matches the master password
# This is done using a SHA256 hash of the password
def verify_password(password):
    password = bytes(password, encoding='utf-8')                                                    # Converts password to bytes
    logger.log_event('Verifying password...', __name__)
    verification_location = os.path.dirname(os.path.abspath(__file__)) + "/../keys/verify.key"      # Stores location of verification file (i.e. result of hash of master password)

    digest = hashes.Hash(hashes.SHA256())                                                           # Prepares the SHA256 Hashing algorithm
    digest.update(password)
    hashed_password = digest.finalize()                                                             # Hashes the entered password

    if not os.path.isfile(verification_location):                                                   # Checks if the verification file exists (i.e. has a master password been setup?)
        # Old password not found                                                                    # No old password was found, so this becomes the new password
        logger.log_event('Previous password missing. Saving this as new password.', __name__)
        f = open(verification_location, 'wb')
        f.write(hashed_password)                                                                    # Stores the hash of the new master password to verify the password next time
        return True
    else:
        logger.log_event('Found previous password. Verfying.', __name__)                            # An old password was found, should check the new password against it
        f = open(verification_location, 'rb')
        old_hash = f.readline()
        if old_hash == hashed_password:                                                             # If the two hashes are equal, then the password matches
            logger.log_event('Password matched.', __name__)
            return True
        logger.log_event('Password did not match.', __name__)
        return False

# Returns true if a master password has been set up
def check_master_exists():
    verification_location = os.path.dirname(os.path.abspath(__file__)) + "/../keys/verify.key"
    return os.path.isfile(verification_location)