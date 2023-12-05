import logger
logger.log_event('Started process', __name__)
import db_manager
import password_manager

success = False
while not success:
    password = input("Enter your password: ")
    success = password_manager.login(password)
    print(success)