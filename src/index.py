import logger
logger.log_event('Started process', __name__)
import db_manager
import password_manager

success = False
while not success:
    password = input("Enter your password: ")
    success = password_manager.login(password)
    print(success)

message = input('Enter a message: ')
enc = password_manager.encrypt(message)
print(enc)
dec = password_manager.decrypt(enc)
print(dec)