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
    logger.log_event("Generating master key from master password", __name__)
    password = bytes(password, encoding='utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=gen_or_get_salt(),
        iterations=480000,
    )
    key = kdf.derive(password)
    return key
    

def verify_password(password):
    password = bytes(password, encoding='utf-8')
    logger.log_event('Verifying password...', __name__)
    verification_location = os.path.dirname(os.path.abspath(__file__)) + "/../keys/verify.key"

    digest = hashes.Hash(hashes.SHA256())
    digest.update(password)
    hashed_password = digest.finalize()

    if not os.path.isfile(verification_location):
        # Old password not found
        logger.log_event('Previous password missing. Saving this as new password.', __name__)
        f = open(verification_location, 'wb')
        f.write(hashed_password)
        return True
    else:
        logger.log_event('Found previous password. Verfying.', __name__)
        f = open(verification_location, 'rb')
        old_hash = f.readline()
        if old_hash == hashed_password:
            logger.log_event('Password matched.', __name__)
            return True
        logger.log_event('Password did not match.', __name__)
        return False


def check_master_exists():
    verification_location = os.path.dirname(os.path.abspath(__file__)) + "/../keys/verify.key"
    return os.path.isfile(verification_location)


if __name__ == "__main__":
    password = input("Enter a password: ")
    key = generate_key_from_password(password)
    print(verify_password(password))