import logger
logger.log_event('Started process', __name__)
import db_manager
import password_manager

success = False
while not success:
    password = input("Enter your password: ")
    success = password_manager.login(password)
    print(success)

username = input('Enter username: ')
# password = input('Enter password: ')
url = 'http://google.com'

# password_manager.add_entry(username, password, url)

print(password_manager.get_password_for_entry(username, url))