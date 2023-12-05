import logger
logger.log_event("Starting process", __name__)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

# Reads salt from file if it exists,
# otherwise, generates new salt and saves to file
def gen_or_get_salt():
    logger.log_event('Looking for salt...', __name__)
    salt_location = os.path.dirname(os.path.abspath(__file__)) + "/../keys/salt.key"
    salt = b''
    if os.path.isfile(salt_location):
        logger.log_event('Salt found!', __name__)
        # read salt from file
        f = open(salt_location, 'rb')
        salt = f.readline()
        f.close()
    else:
        logger.log_event('Salt not found. Generating Salt', __name__)
        salt = os.urandom(16)
        f = open(salt_location, 'wb')
        f.write(salt)
        f.close()
    
    return salt

def generate_key_from_password(password):
    logger.log_event("Generating master key from master password")
    

if __name__ == "__main__":
    print(gen_or_get_salt())